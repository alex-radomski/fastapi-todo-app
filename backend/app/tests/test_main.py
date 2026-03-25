from fastapi.testclient import TestClient

from ..models import CreateTodo
from ..repository import Repository


def test_root_returns_all_todos(client: TestClient, repository: Repository) -> None:
    todo_1 = repository.save_todo(CreateTodo(task_name="Buy milk", is_done=False))
    todo_2 = repository.save_todo(CreateTodo(task_name="Walk the dog", is_done=True))

    response = client.get("/")

    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2
    assert todos[0]["id"] == todo_1.id
    assert todos[0]["task_name"] == "Buy milk"
    assert todos[0]["is_done"] is False

    assert todos[1]["id"] == todo_2.id
    assert todos[1]["task_name"] == "Walk the dog"
    assert todos[1]["is_done"] is True
