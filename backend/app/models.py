from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# SQLAlchemy models — represent database tables
class Base(DeclarativeBase):
    pass


class TodoDB(Base):
    __tablename__ = "to_dos"
    id: Mapped[str] = mapped_column(primary_key=True)
    task_name: Mapped[str] = mapped_column()
    is_done: Mapped[bool] = mapped_column()


# Pydantic models — represent API inputs and outputs
class CreateTodo(BaseModel):
    task_name: str
    is_done: bool


class Todo(BaseModel):
    id: str
    task_name: str
    is_done: bool


class UserSchema(BaseModel):
    id: int
    user: str


class UpdateTodo(BaseModel):
    id: str
    task_name: str | None = None
    is_done: bool | None = None
