#!/usr/bin/env bash
# Integration tests on a throwaway ERPNext v15 site in Docker, as CI runs them.
#   bash .github/ci/integration.sh          (KEEP=1 leaves the containers running)
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-erpnext-iran-ci}"
export MSYS_NO_PATHCONV=1 # Git Bash on Windows: keep container paths as they are

compose() { docker compose -f docker-compose.yml "$@"; }
in_bench() { compose exec -T erpnext bash -lc "cd /home/frappe/frappe-bench && $1"; }

compose up -d
trap '[ -n "${KEEP:-}" ] || compose down -v' EXIT

in_bench "bash apps/erpnext_iran/.github/ci/setup_site.sh"

compose exec -T -d erpnext bash -lc "cd /home/frappe/frappe-bench && bench serve --port 8000 > /tmp/serve.log 2>&1"
in_bench 'for _ in $(seq 60); do curl -sf http://127.0.0.1:8000/api/method/ping > /dev/null && exit 0; sleep 2; done; cat /tmp/serve.log; exit 1'

# ERPNext's setup wizard (root groups, a company), as `run-tests` does before its first test
in_bench "bench --site test.localhost execute erpnext.setup.utils.before_tests"
in_bench "bench --site test.localhost execute erpnext_iran.tests.demo.make"
# bench run-tests can exit 0 with failed tests: judge by unittest's summary line
in_bench "bench --site test.localhost run-tests --module erpnext_iran.tests.test_integration 2>&1 | tee /tmp/tests.log"
in_bench 'grep -q "^Ran [0-9]* test" /tmp/tests.log && grep -qx "OK" /tmp/tests.log'
