import os
from typing import Iterator
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from .models import CreateTodo, Todo, TodoDB

load_dotenv()
engine = create_engine(os.getenv("DB_URL"), echo=False)  # type: ignore
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Database Dependency
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Repository:
    # Accepts a database session on creation so all methods can use the same connection.
    def __init__(self, session: Session):
        self.session = session

    def save_todo(self, todo: CreateTodo) -> Todo:
        db_todo = TodoDB(
            id=str(uuid4()), task_name=todo.task_name, is_done=todo.is_done
        )
        self.session.add(db_todo)
        self.session.commit()
        return Todo(id=db_todo.id, task_name=db_todo.task_name, is_done=db_todo.is_done)

    def load_all_todos(self) -> list[Todo]:
        stmt = select(TodoDB)
        results = list(self.session.execute(stmt).scalars().all())
        return [
            Todo(id=todo.id, task_name=todo.task_name, is_done=todo.is_done)
            for todo in results
        ]

    def load_todo_by_id(self, todo_id: str) -> Todo | None:
        stmt = select(TodoDB).where(TodoDB.id == todo_id)
        db_todo = self.session.execute(stmt).scalar_one_or_none()

        return (
            Todo(id=db_todo.id, task_name=db_todo.task_name, is_done=db_todo.is_done)
            if db_todo
            else None
        )
