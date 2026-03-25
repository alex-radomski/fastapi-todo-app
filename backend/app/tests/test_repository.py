from ..models import CreateTodo
from ..repository import Repository

# 'repository' is a pytest fixture defined in conftest.py.
# pytest automatically creates a Repository instance and passes it into each test — you don't call it yourself.


class TestRepository:
    def test_save_and_load_todo(self, repository: Repository) -> None:

        todo = repository.save_todo(
            CreateTodo(task_name="Buy groceries", is_done=False)
        )

        loaded_todo = repository.load_todo_by_id(todo.id)

        assert loaded_todo is not None
        assert loaded_todo.id == todo.id
        assert loaded_todo.task_name == "Buy groceries"
        assert loaded_todo.is_done is False

    def test_load_all_todos(self, repository: Repository) -> None:

        todo_1 = repository.save_todo(
            CreateTodo(task_name="Buy groceries", is_done=False)
        )
        todo_2 = repository.save_todo(
            CreateTodo(task_name="Walk the dog", is_done=True)
        )

        all_todos = repository.load_all_todos()

        assert len(all_todos) == 2
        assert all_todos[0].id == todo_1.id
        assert all_todos[0].task_name == "Buy groceries"
        assert all_todos[0].is_done is False
        assert all_todos[1].id == todo_2.id
        assert all_todos[1].task_name == "Walk the dog"
        assert all_todos[1].is_done is True
