import pytest
from fastapi.testclient import TestClient
from app.main import app, registry

client = TestClient(app)

def test_register_and_list():
    # register a worker
    resp = client.post('/workers/register', json={"id": "test-w", "url": "http://127.0.0.1:9999"})
    assert resp.status_code == 200
    data = client.get('/workers')
    assert data.status_code == 200
    workers = data.json()
    assert any(w['id'] == 'test-w' for w in workers)

def test_predict_no_workers():
    # create a fresh registry, monkeypatch the app.registry if needed
    # but here we use the global registry; first remove any workers
    for w in list(registry.list_workers()):
        # direct manipulation for test cleanup
        registry._workers.pop(w['id'], None)
    resp = client.post('/predict', json={"input": [0.1]*8})
    assert resp.status_code == 503
