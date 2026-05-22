from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_get_task():
    # Crée une tâche
    res = client.post("/tasks", json={"title": "Test task"})
    assert res.status_code == 201
    assert res.json()["title"] == "Test task"
    assert res.json()["done"] == False