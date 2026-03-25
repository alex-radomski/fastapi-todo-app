from ..models import ToDo
from ..repository import Repository

# 'repository' is a pytest fixture defined in conftest.py.
# pytest automatically creates a Repository instance and passes it into each test — you don't call it yourself.


class TestRepository:
    def test_save_and_load_todo(self, repository: Repository):

        todo = ToDo(id="1", task_name="Buy groceries", is_done=False)

        repository.save_todo(todo)

        loaded_todo = repository.load_todo_by_id("1")

        assert loaded_todo is not None
        assert loaded_todo.id == "1"
        assert loaded_todo.task_name == "Buy groceries"
        assert loaded_todo.is_done is False

    def test_load_all_todos(self, repository: Repository):

        todo1 = ToDo(id="1", task_name="Buy groceries", is_done=False)
        todo2 = ToDo(id="2", task_name="Walk the dog", is_done=True)

        repository.save_todo(todo1)
        repository.save_todo(todo2)

        all_todos = repository.load_all_todos()

        assert len(all_todos) == 2
        assert all_todos[0].id == "1"
        assert all_todos[0].task_name == "Buy groceries"
        assert all_todos[0].is_done is False
        assert all_todos[1].id == "2"
        assert all_todos[1].task_name == "Walk the dog"
        assert all_todos[1].is_done is True
