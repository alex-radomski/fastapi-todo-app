from uuid import uuid4

import pytest

from ..models import CreateTodo, UpdateTodo
from ..repository import Repository

# 'repository' is a pytest fixture defined in conftest.py.
# pytest automatically creates a Repository instance and passes it into each test — you don't call it yourself.


class TestRepository:
    def test_save_and_load_todo(self, repository: Repository) -> None:
        todo = repository.save_todo(
            CreateTodo(task_name="do the washing", is_done=False)
        )
        loaded_todo = repository.load_todo_by_id(todo.id)

        assert loaded_todo is not None
        assert loaded_todo.id == todo.id
        assert loaded_todo.task_name == todo.task_name
        assert loaded_todo.is_done == todo.is_done

    def test_save_and_load_todos(self, repository: Repository) -> None:
        todo = repository.save_todo(
            CreateTodo(task_name="do the washing", is_done=False)
        )
        todo2 = repository.save_todo(
            CreateTodo(task_name="take Shadow out", is_done=True)
        )
        todo3 = repository.save_todo(
            CreateTodo(task_name="finish the assignment", is_done=False)
        )
        loaded_todos = repository.load_all_todos()

        assert len(loaded_todos) == 3
        assert loaded_todos is not None

        assert loaded_todos[0].id == todo.id
        assert loaded_todos[0].task_name == todo.task_name
        assert loaded_todos[0].is_done == todo.is_done

        assert loaded_todos[1].id == todo2.id
        assert loaded_todos[1].task_name == todo2.task_name
        assert loaded_todos[1].is_done == todo2.is_done

        assert loaded_todos[2].id == todo3.id
        assert loaded_todos[2].task_name == todo3.task_name
        assert loaded_todos[2].is_done == todo3.is_done

    def test_load_todo_by_id_raises_error_if_not_found(
        self, repository: Repository
    ) -> None:

        with pytest.raises(Exception, match="Todo with id '12345' not found"):
            repository.load_todo_by_id("12345")

    def test_delete_todo_by_id(self, repository: Repository) -> None:
        todo = repository.save_todo(
            CreateTodo(task_name="do the washing", is_done=False)
        )
        repository.delete_todo_by_id(todo.id)

        with pytest.raises(Exception, match=f"Todo with id '{todo.id}' not found"):
            repository.load_todo_by_id(todo.id)

    def test_delete_todo_only_deletes_intended_todo(
        self, repository: Repository
    ) -> None:
        todo = repository.save_todo(
            CreateTodo(task_name="do the washing", is_done=False)
        )
        todo2 = repository.save_todo(
            CreateTodo(task_name="take Shadow out", is_done=True)
        )
        repository.delete_todo_by_id(todo.id)

        loaded_todo2 = repository.load_todo_by_id(todo2.id)

        assert loaded_todo2 == todo2

    def test_delete_todo_does_not_exist_raises_error(
        self, repository: Repository
    ) -> None:

        fake_id = str(uuid4())
        with pytest.raises(Exception, match=f"Todo with id '{fake_id}' not found"):
            repository.delete_todo_by_id(fake_id)

    def test_update_todo_task_name(self, repository: Repository) -> None:
        original_todo = repository.save_todo(
            CreateTodo(task_name="do the washing", is_done=False)
        )

        repository.update_todo(
            UpdateTodo(id=original_todo.id, task_name="do the dishes")
        )

        updated_loaded_todo = repository.load_todo_by_id(original_todo.id)
        assert updated_loaded_todo is not None
        assert updated_loaded_todo.id == original_todo.id
        assert updated_loaded_todo.task_name == "do the dishes"
        assert updated_loaded_todo.is_done == original_todo.is_done

    def test_update_todo_is_done(self, repository: Repository) -> None:
        original_todo = repository.save_todo(
            CreateTodo(task_name="do the washing", is_done=False)
        )

        repository.update_todo(UpdateTodo(id=original_todo.id, is_done=True))

        updated_loaded_todo = repository.load_todo_by_id(original_todo.id)
        assert updated_loaded_todo is not None
        assert updated_loaded_todo.id == original_todo.id
        assert updated_loaded_todo.task_name == original_todo.task_name
        assert updated_loaded_todo.is_done is True

    def test_update_todo_all_fields(self) -> None: ...

    def test_update_todo_does_not_exist_raises_error(self) -> None: ...
