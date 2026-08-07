#!/bin/sh
set -eu

export PROMETHEUS_MULTIPROC_DIR="${PROMETHEUS_MULTIPROC_DIR:-/tmp/prometheus-multiproc}"
if [ "${PORT:-3000}" = "${METRICS_PORT:-9090}" ]; then
    echo "PORT and METRICS_PORT must be different" >&2
    exit 1
fi
mkdir -p "$PROMETHEUS_MULTIPROC_DIR"
find "$PROMETHEUS_MULTIPROC_DIR" -type f -delete

gunicorn \
    --workers 1 \
    --bind "0.0.0.0:${METRICS_PORT:-9090}" \
    --no-control-socket \
    --access-logfile - \
    --error-logfile - \
    metrics_app:app &
metrics_pid=$!

terminate() {
    if [ -n "${app_pid:-}" ]; then
        kill -TERM "$app_pid" 2>/dev/null || true
    fi
    kill -TERM "$metrics_pid" 2>/dev/null || true
}
trap 'terminate; exit 143' INT TERM

gunicorn \
    --config python:gunicorn_metrics \
    --workers "${WEB_CONCURRENCY:-2}" \
    --bind "0.0.0.0:${PORT:-3000}" \
    --no-control-socket \
    --timeout "${GUNICORN_TIMEOUT:-600}" \
    main:app &
app_pid=$!

while kill -0 "$app_pid" 2>/dev/null && kill -0 "$metrics_pid" 2>/dev/null; do
    sleep 1
done

status=1
if ! kill -0 "$app_pid" 2>/dev/null; then
    set +e
    wait "$app_pid"
    status=$?
    set -e
fi
terminate
wait "$app_pid" 2>/dev/null || true
wait "$metrics_pid" 2>/dev/null || true
exit "$status"
