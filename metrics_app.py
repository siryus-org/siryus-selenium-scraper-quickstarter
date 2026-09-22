import os

from prometheus_client import CONTENT_TYPE_LATEST, REGISTRY, CollectorRegistry, generate_latest, multiprocess
from selenium_scraper_runtime.metrics import BUILD_INFO

_ = BUILD_INFO


def _registry():
    if os.getenv("PROMETHEUS_MULTIPROC_DIR"):
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        return registry
    return REGISTRY


def app(environ, start_response):
    if environ.get("PATH_INFO") == "/-/healthy":
        body = b"ok\n"
        start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
        return [body]
    if environ.get("PATH_INFO") != "/metrics":
        body = b"not found\n"
        start_response("404 Not Found", [("Content-Type", "text/plain"), ("Content-Length", str(len(body)))])
        return [body]

    body = generate_latest(_registry())
    start_response("200 OK", [("Content-Type", CONTENT_TYPE_LATEST), ("Content-Length", str(len(body)))])
    return [body]
