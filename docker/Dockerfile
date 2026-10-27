# Ready ERPNext image with Frappe HR and erpnext_iran (published to ghcr.io by release.yml).
#   docker build -f docker/Dockerfile --build-arg ERPNEXT_VERSION=version-15 -t erpnext-iran .
# Use it in place of frappe/erpnext in frappe_docker's compose files.
ARG ERPNEXT_VERSION=version-15
FROM frappe/erpnext:${ERPNEXT_VERSION}
ARG ERPNEXT_VERSION

USER frappe
WORKDIR /home/frappe/frappe-bench
COPY --chown=frappe:frappe . apps/erpnext_iran

# erpnext_iran is installed first: bench imports every app under apps/ when it builds
RUN bash -lc '\
	set -e; \
	./env/bin/pip install --no-cache-dir -e apps/erpnext_iran; \
	yarn config set network-timeout 600000 > /dev/null; \
	bench get-app hrms --branch "$ERPNEXT_VERSION"; \
	grep -qx erpnext_iran sites/apps.txt || printf "\nerpnext_iran\n" >> sites/apps.txt; \
	sed -i "/^$/d" sites/apps.txt; \
	bench build --app erpnext_iran'

LABEL org.opencontainers.image.source="https://github.com/bijanshdevops/erpnext_iran" \
	org.opencontainers.image.description="ERPNext with Frappe HR and erpnext_iran (Iranian localization)" \
	org.opencontainers.image.licenses="GPL-3.0"
