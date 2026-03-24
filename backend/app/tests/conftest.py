import psycopg
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from sqlalchemy.engine import URL
from typing import Iterator

from ..db_models import Base


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    conn = psycopg.connect(
        host="localhost",
        port=5433,
        user="todo",
        password="todo",
        dbname="postgres",
        autocommit=True,
    )
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'todo_test'")
    if not cursor.fetchone():
        cursor.execute("CREATE DATABASE todo_test")

    yield

    cursor.execute("DROP DATABASE todo_test WITH (FORCE)")
    conn.close()


@pytest.fixture
def database_engine(setup_test_database):
    url = URL.create(
        "postgresql+psycopg",
        username="todo",
        password="todo",
        host="localhost",
        port=5433,
        database="todo_test",
    )
    engine = create_engine(url, poolclass=NullPool)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    yield engine
    engine.dispose()


@pytest.fixture
def database_session(database_engine) -> Iterator[Session]:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
