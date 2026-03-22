from pydantic import BaseModel

class ToDo(BaseModel):
    id: str
    task: str
    is_done: bool


class User(BaseModel):
    id: int
    user: str
