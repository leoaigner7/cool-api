from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_upsert_and_list():
    payload = {"k": "hello", "v": "world"}
    r = client.put("/kv", json=payload)
    assert r.status_code == 200
    r = client.get("/kv")
    assert r.status_code == 200
    data = r.json()
    assert any(item["k"] == "hello" and item["v"] == "world" for item in data)

