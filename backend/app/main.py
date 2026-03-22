from fastapi import FastAPI, Depends
from pydantic import BaseModel, ValidationError
from .db import engine, get_db
from .db_models import Base, ToDo
from sqlalchemy.orm import Session



app = FastAPI()
Base.metadata.create_all(engine)

@app.get("/")
async def root(db: Session = Depends(get_db)):

    new_todo = ToDo(id ="this is the id", task_name="Sample ToDo", is_done= False)

    db.add(new_todo)
    db.commit()



    return {"message": "Hello World"}