from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session
from .db_models import ToDo

load_dotenv()


engine = create_engine(os.getenv("DB_URL"), echo=True) # type: ignore

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_todo(db: Session, id: str, task_name: str, is_done: bool = False):
    todo = ToDo(id=id, task_name=task_name, is_done=is_done)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todo(db: Session, id: str):
    return db.get(ToDo, id)