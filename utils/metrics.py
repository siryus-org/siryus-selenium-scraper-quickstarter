import os
import time

from flask import g, request
from prometheus_client import Counter, Gauge, Histogram


SERVICE_NAME = os.getenv("SCRAPER_SERVICE_NAME", "selenium-scraper-quickstarter")

HTTP_REQUESTS = Counter(
    "scraper_http_requests_total",
    "Total HTTP requests handled by the scraper API.",
    ("service", "method", "endpoint", "status", "outcome"),
)
HTTP_REQUEST_DURATION = Histogram(
    "scraper_http_request_duration_seconds",
    "Scraper API request duration in seconds.",
    ("service", "method", "endpoint"),
    buckets=(0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30, 60, 120, 300, 600),
)
HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "scraper_http_requests_in_progress",
    "Scraper API requests currently in progress.",
    ("service",),
    multiprocess_mode="livesum",
)
UNHANDLED_EXCEPTIONS = Counter(
    "scraper_unhandled_exceptions_total",
    "Unhandled exceptions raised while serving scraper API requests.",
    ("service", "endpoint"),
)
BUILD_INFO = Gauge(
    "scraper_build_info",
    "Scraper service identity.",
    ("service",),
    multiprocess_mode="livemax",
)
BUILD_INFO.labels(service=SERVICE_NAME).set(1)


def _endpoint():
    return request.url_rule.rule if request.url_rule else "unmatched"


def init_metrics(app):
    @app.before_request
    def observe_request_start():
        g.metrics_start_time = time.monotonic()
        HTTP_REQUESTS_IN_PROGRESS.labels(service=SERVICE_NAME).inc()

    @app.after_request
    def observe_request_end(response):
        start_time = getattr(g, "metrics_start_time", None)
        endpoint = _endpoint()
        outcome = "success" if response.status_code < 400 else "error"
        HTTP_REQUESTS.labels(
            service=SERVICE_NAME,
            method=request.method,
            endpoint=endpoint,
            status=str(response.status_code),
            outcome=outcome,
        ).inc()
        if start_time is not None:
            HTTP_REQUEST_DURATION.labels(
                service=SERVICE_NAME,
                method=request.method,
                endpoint=endpoint,
            ).observe(time.monotonic() - start_time)
            HTTP_REQUESTS_IN_PROGRESS.labels(service=SERVICE_NAME).dec()
            g.metrics_start_time = None
        return response

    @app.teardown_request
    def observe_unhandled_exception(exception):
        if exception is not None:
            UNHANDLED_EXCEPTIONS.labels(
                service=SERVICE_NAME,
                endpoint=_endpoint(),
            ).inc()
            if getattr(g, "metrics_start_time", None) is not None:
                HTTP_REQUESTS_IN_PROGRESS.labels(service=SERVICE_NAME).dec()
                g.metrics_start_time = None
