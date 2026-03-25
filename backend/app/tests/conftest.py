from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from ..main import app
from ..models import Base
from ..repository import Repository, get_db


# Connects to the test database and recreates all tables before each test,
# so every test starts with a clean, empty database.
@pytest.fixture
def database_engine() -> Iterator[Engine]:
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


# Wraps the session in our Repository class so tests can call methods like
# save_todo() and load_todo() directly.
@pytest.fixture
def repository(database_session: Session) -> Repository:
    return Repository(database_session)


# Provides an HTTP test client for making requests against the app (e.g. client.get("/")).
# Swaps out the real database for the test one so requests hit test data, not production.
@pytest.fixture
def client(database_session: Session) -> Iterator[TestClient]:
    app.dependency_overrides[get_db] = lambda: database_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Opens a database session for the duration of a single test,
# then closes it when the test finishes.
@pytest.fixture
def database_session(database_engine: Engine) -> Iterator[Session]:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
