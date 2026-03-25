from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .models import Todo
from .repository import Repository, get_db

app = FastAPI()


@app.get("/")
def get_todos(database: Session = Depends(get_db)) -> list[Todo]:
    return Repository(database).load_all_todos()
