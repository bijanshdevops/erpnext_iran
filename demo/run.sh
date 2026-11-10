#!/bin/bash
# demo-reset service of compose.demo.yml: creates the demo site on first start, keeps a backup of
# it as the baseline, and restores that backup every RESET_HOURS hours.
set -euo pipefail
cd /home/frappe/frappe-bench

# kept in the sites volume, which the frappe user can write to
BASELINE=/home/frappe/frappe-bench/sites/demo-baseline
root=(--db-root-username root --db-root-password "$DB_ROOT_PASSWORD")

# ERPNext builds its caches on the first requests after a start or a cache clear, which takes
# many seconds; make them here rather than in a visitor's first page load.
warm_up() {
	local jar
	jar=$(mktemp)
	wait-for-it -q -t 120 frontend:8080 || return 0
	for _ in 1 2 3 4; do
		curl -s -o /dev/null http://frontend:8080/login
		curl -s -o /dev/null -c "$jar" -H "Content-Type: application/json" 			-d "{\"usr\": \"$DEMO_USER\", \"pwd\": \"$DEMO_PASSWORD\"}" http://frontend:8080/api/method/login
		curl -s -o /dev/null -b "$jar" http://frontend:8080/app/home
		for doctype in "Sales%20Invoice" "Purchase%20Invoice" "Item" "Customer" "IR%20Cheque" "Salary%20Slip"; do
			curl -s -o /dev/null -b "$jar" "http://frontend:8080/api/method/frappe.desk.form.load.getdoctype?doctype=$doctype"
		done
	done
	rm -f "$jar"
	echo "$(date -Is) caches warmed"
}

wait-for-it -t 300 db:3306
wait-for-it -t 120 redis-cache:6379
wait-for-it -t 120 redis-queue:6379

if [ ! -f "sites/$SITE/site_config.json" ] || ! ls "$BASELINE"/*-database.sql.gz > /dev/null 2>&1; then
	echo "Creating the demo site $SITE"
	rm -rf "sites/$SITE" "$BASELINE"
	mkdir -p "$BASELINE"
	bench new-site "$SITE" --force "${root[@]}" --mariadb-user-host-login-scope='%' --admin-password "$ADMIN_PASSWORD" \
		--install-app erpnext --install-app hrms --install-app erpnext_iran
	bench --site "$SITE" set-config erpnext_iran_demo_user "$DEMO_USER"
	bench --site "$SITE" set-config -p mute_emails 1
	bench --site "$SITE" set-config host_name "https://$SITE"
	bench --site "$SITE" execute erpnext_iran.demo_site.setup \
		--kwargs "{\"user\": \"$DEMO_USER\", \"password\": \"$DEMO_PASSWORD\", \"reset_hours\": $RESET_HOURS}"
	bench --site "$SITE" scheduler disable
	bench --site "$SITE" backup --backup-path "$BASELINE"
	echo "Demo site ready"
fi
warm_up

while true; do
	sleep "$((RESET_HOURS * 3600))"
	echo "$(date -Is) resetting the demo site"
	bench --site "$SITE" restore "$(ls "$BASELINE"/*-database.sql.gz | head -1)" "${root[@]}" --force
	find "sites/$SITE/public/files" "sites/$SITE/private/files" -mindepth 1 -delete 2> /dev/null || true
	bench --site "$SITE" clear-cache
	warm_up
done
