import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import ToDo

load_dotenv()
engine = create_engine(os.getenv("DB_URL"), echo=True)  # type: ignore
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Repository:
    # Accepts a database session on creation so all methods can use the same connection.
    def __init__(self, session: Session):
        self.session = session

    def save_todo(self, todo: ToDo):
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def load_todo_by_id(self, todo_id: str):
        return self.session.query(ToDo).filter(ToDo.id == todo_id).first()

    def load_all_todos(self):
        return self.session.query(ToDo).all()
