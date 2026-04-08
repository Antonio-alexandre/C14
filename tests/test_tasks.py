from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    response = client.post("/tasks", json={"title": "Viagem para Ouro Preto"})
    assert response.status_code == 200
    assert response.json()["title"] == "Viagem para Ouro Preto"

def test_list_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task_by_id():
    create = client.post("/tasks", json={"title": "Jogar JUMS"})
    task_id = create.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task():
    create = client.post("/tasks", json={"title": "Estudar C08"})
    task_id = create.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Estudar C14"})
    assert response.status_code == 200
    assert response.json()["title"] == "Estudar C14"

def test_delete_task():
    create = client.post("/tasks", json={"title": "Festa dos alunos"})
    task_id = create.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

def test_mark_task_completed():
    create = client.post("/tasks", json={"title": "Calourada"})
    task_id = create.json()["id"]

    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_multiple_tasks():
    client.post("/tasks", json={"title": "Prova de C08"})
    client.post("/tasks", json={"title": "Prova de T106"})

    response = client.get("/tasks")
    assert len(response.json()) >= 2

def test_task_has_default_completed_false():
    response = client.post("/tasks", json={"title": "Treino de handebol"})
    assert response.json()["completed"] is False

def test_update_task_description():
    create = client.post("/tasks", json={"title": "Treino de volêi"})
    task_id = create.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Treino de volêi", "description": "O treino foi ruim"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "O treino foi ruim"

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_task_without_title():
    response = client.post("/tasks", json={})
    assert response.status_code == 422

def test_get_nonexistent_task():
    response = client.get("/tasks/9999")
    assert response.status_code == 404

def test_update_nonexistent_task():
    response = client.put("/tasks/9999", json={"title": "Treino de futsal"})
    assert response.status_code == 404

def test_delete_nonexistent_task():
    response = client.delete("/tasks/9999")
    assert response.status_code == 404

def test_complete_nonexistent_task():
    response = client.patch("/tasks/9999/complete")
    assert response.status_code == 404

def test_invalid_id_type():
    response = client.get("/tasks/abc")
    assert response.status_code == 422

def test_update_with_invalid_body():
    create = client.post("/tasks", json={"title": "Campeonato de LOL"})
    task_id = create.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={})
    assert response.status_code == 422

def test_delete_twice():
    create = client.post("/tasks", json={"title": "Fazer almoço"})
    task_id = create.json()["id"]

    client.delete(f"/tasks/{task_id}")
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_complete_twice():
    create = client.post("/tasks", json={"title": "Fazer janta"})
    task_id = create.json()["id"]

    client.patch(f"/tasks/{task_id}/complete")
    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200

def test_empty_task_list():
    response = client.get("/tasks")
    assert response.status_code == 200