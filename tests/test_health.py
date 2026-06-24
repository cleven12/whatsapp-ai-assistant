def test_health_endpoint(client):
    """Basic smoke test for the health route."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
