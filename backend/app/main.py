from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .repository import Repository, get_db

app = FastAPI()


@app.get("/")
async def root(database: Session = Depends(get_db)):
    return Repository(database).load_all_todos()
