import json

def test_webhook_verify_success(client, app):
    """Test the GET verification handshake."""
    verify_token = app.config["WHATSAPP_VERIFY_TOKEN"]
    resp = client.get(f"/webhook/?hub.mode=subscribe&hub.verify_token={verify_token}&hub.challenge=challenge123")
    assert resp.status_code == 200
    assert resp.data.decode() == "challenge123"

def test_webhook_verify_fail(client):
    resp = client.get("/webhook/?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=xx")
    assert resp.status_code == 403

def test_webhook_post_ignored(client):
    """Empty or bad payload should be ignored gracefully."""
    resp = client.post("/webhook/", json={})
    assert resp.status_code == 200
    assert resp.json["status"] == "ignored"
