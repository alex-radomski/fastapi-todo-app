from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass

class ToDo(Base):
    __tablename__ = "to_dos"
    id: Mapped[str] = mapped_column(primary_key=True)
    task_name: Mapped[str] = mapped_column()
    is_done: Mapped[bool] = mapped_column()
    