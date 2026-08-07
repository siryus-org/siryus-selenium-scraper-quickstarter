from prometheus_client import generate_latest

from main import app


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
