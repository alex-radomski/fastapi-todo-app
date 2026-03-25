from ..models import ToDo
from ..repository import Repository


def test_root_returns_all_todos(client, repository: Repository):
    repository.save_todo(ToDo(id="1", task_name="Buy milk", is_done=False))
    repository.save_todo(ToDo(id="2", task_name="Walk the dog", is_done=True))

    response = client.get("/")

    assert response.status_code == 200
    todos = response.json()
    assert len(todos) == 2
    assert todos[0]["task_name"] == "Buy milk"
    assert todos[1]["task_name"] == "Walk the dog"
