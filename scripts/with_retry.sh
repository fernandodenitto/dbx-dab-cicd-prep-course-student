#!/usr/bin/env bash
# Run a command; if it fails because serverless capacity is exhausted, wait and retry.
# Any other failure fails immediately — retries must never hide real errors.
#
#   scripts/with_retry.sh databricks bundle run --target staging daily
#
# Free Edition releases serverless compute with a delay: a run that starts seconds after
# another one finished can fail with RESOURCE_EXHAUSTED. On paid workspaces this is rare,
# but capacity errors are transient anywhere, and this is the right shape for them.
set -uo pipefail
attempts=${RETRY_ATTEMPTS:-4}
wait_seconds=${RETRY_WAIT_SECONDS:-90}

for attempt in $(seq 1 "$attempts"); do
  log=$(mktemp)
  "$@" 2>&1 | tee "$log"
  status=${PIPESTATUS[0]}
  if [ "$status" -eq 0 ]; then
    exit 0
  fi
  if ! grep -q "RESOURCE_EXHAUSTED" "$log"; then
    exit "$status"
  fi
  if [ "$attempt" -lt "$attempts" ]; then
    echo "::warning::Serverless capacity exhausted (attempt $attempt/$attempts) — retrying in ${wait_seconds}s"
    sleep "$wait_seconds"
  fi
done
exit "$status"
