#!/bin/bash
# demo-reset service of compose.demo.yml: creates the demo site on first start, keeps a backup of
# it as the baseline, and restores that backup every RESET_HOURS hours.
set -euo pipefail
cd /home/frappe/frappe-bench

# kept in the sites volume, which the frappe user can write to
BASELINE=/home/frappe/frappe-bench/sites/demo-baseline
root=(--db-root-username root --db-root-password "$DB_ROOT_PASSWORD")

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

while true; do
	sleep "$((RESET_HOURS * 3600))"
	echo "$(date -Is) resetting the demo site"
	bench --site "$SITE" restore "$(ls "$BASELINE"/*-database.sql.gz | head -1)" "${root[@]}" --force
	find "sites/$SITE/public/files" "sites/$SITE/private/files" -mindepth 1 -delete 2> /dev/null || true
	bench --site "$SITE" clear-cache
done
