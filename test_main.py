import pytest
from fastapi.testclient import TestClient
from main import app, tasks  # main.py se app aur tasks list import ki

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    tasks.clear()
    yield


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Task Manager API is running!"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_get_all_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == {"total": 0, "tasks": []}


def test_create_task_success():
    payload = {"name": "Learn Pytest", "is_done": False}
    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    assert response.json()["message"] == "Task created successfully"
    assert response.json()["task"]["name"] == "Learn Pytest"
    assert response.json()["total_tasks"] == 1


def test_create_task_empty_name_error():
    payload = {"name": "   ", "is_done": False}
    response = client.post("/tasks", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Task name cannot be empty"


def test_get_single_task_success():
    tasks.append({"name": "Buy Milk", "is_done": False})

    response = client.get("/tasks/0")
    assert response.status_code == 200
    assert response.json()["name"] == "Buy Milk"
    assert response.json()["status"] == "not done yet"


def test_get_single_task_not_found():
    response = client.get("/tasks/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task_success():
    tasks.append({"name": "Old Task", "is_done": False})

    updated_payload = {"name": "Updated Task", "is_done": True}
    response = client.put("/tasks/0", json=updated_payload)

    # assert response.status_code == 200
    assert response.json()["message"] == "Task updated"
    assert response.json()["task"]["is_done"] is True


def test_delete_task_success():
    tasks.append({"name": "Task to Delete", "is_done": False})

    response = client.delete("/tasks/0")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"
    assert response.json()["remaining_tasks"] == 0
