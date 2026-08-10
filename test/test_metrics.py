from prometheus_client import generate_latest

from main import app
from utils.metrics import track_task


def test_metrics_track_successful_and_failed_requests():
    app.config["TESTING"] = True
    with app.test_client() as client:
        assert client.get("/").status_code == 200
        assert client.get("/sample", json={}).status_code == 401

    metrics = generate_latest().decode("utf-8")
    assert 'scraper_http_requests_total{' in metrics
    assert 'endpoint="/"' in metrics
    assert 'outcome="success"' in metrics
    assert 'endpoint="/sample"' in metrics
    assert 'outcome="error"' in metrics


def test_metrics_are_not_served_by_the_application_port():
    app.config["TESTING"] = True
    with app.test_client() as client:
        assert client.get("/metrics").status_code == 404


def test_metrics_track_internal_tasks_and_last_activity():
    with app.test_client() as client:
        assert client.get("/").status_code == 200
    with track_task("scheduled_test"):
        pass

    metrics = generate_latest().decode("utf-8")
    assert 'scraper_task_runs_total{' in metrics
    assert 'task="scheduled_test"' in metrics
    assert 'scraper_task_last_success_timestamp_seconds{' in metrics
    assert 'scraper_http_last_success_timestamp_seconds{' in metrics
