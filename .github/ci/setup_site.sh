#!/usr/bin/env bash
# Runs inside the erpnext container: a fresh site with erpnext and erpnext_iran, built assets.
set -euo pipefail
cd /home/frappe/frappe-bench

for _ in $(seq 60); do
	mysqladmin ping -h db -uroot -padmin --silent && break
	sleep 2
done

bench set-config -g db_host db
bench set-config -g redis_cache redis://redis:6379
bench set-config -g redis_queue redis://redis:6379
bench set-config -g redis_socketio redis://redis:6379

source ~/.nvm/nvm.sh

# bench imports every app under apps/, so erpnext_iran must be installed before any bench build
./env/bin/pip install --quiet -e apps/erpnext_iran

# Frappe HR for the payroll tests; fetched before erpnext_iran is listed, so erpnext_iran stays
# last in apps.txt and its template overrides win
yarn config set network-timeout 600000 > /dev/null # its frontend pulls many packages
for attempt in 1 2 3; do
	[ -d apps/hrms ] && break
	bench get-app hrms --branch version-15 && break
	echo "get-app hrms failed (attempt $attempt), retrying"
	rm -rf apps/hrms
	sed -i '/^hrms$/d' sites/apps.txt
done
[ -d apps/hrms ]

# the image's apps.txt has no trailing newline
grep -qx erpnext_iran sites/apps.txt || printf '\nerpnext_iran\n' >> sites/apps.txt
sed -i '/^$/d' sites/apps.txt

bench new-site test.localhost --mariadb-root-password admin --admin-password admin \
	--mariadb-user-host-login-scope='%' --install-app erpnext --install-app hrms --install-app erpnext_iran
bench use test.localhost
bench --site test.localhost set-config allow_tests true
# PDFs: wkhtmltopdf loads fonts and images from the running site
bench --site test.localhost set-config host_name http://127.0.0.1:8000

bench build --app erpnext_iran
