from ..db import create_todo, get_todo


def test_create_todo(database_session):
    todo = create_todo(database_session, id="1", task_name="Buy groceries", is_done=False)

    assert todo.id == "1"
    assert todo.task_name == "Buy groceries"
    assert todo.is_done is False


def test_todo_persistence(database_session):
    create_todo(database_session, id="2", task_name="Walk the dog", is_done=True)
    database_session.expire_all()

    fetched = get_todo(database_session, "2")

    assert fetched is not None
    assert fetched.id == "2"
    assert fetched.task_name == "Walk the dog"
    assert fetched.is_done is True
