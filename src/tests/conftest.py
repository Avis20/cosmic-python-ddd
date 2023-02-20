# ./src/tests/conftest.py

import pytest

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from app.models.database import BaseModel
from app.settings import get_settings

settings = get_settings()

@pytest.fixture()
def db_in_memory():
    engine = create_engine("sqlite:///:memory:")
    # Для test_api
    # engine = create_engine(settings.get_postgres_uri)
    BaseModel.metadata.create_all(engine)
    return engine



@pytest.fixture
def session(db_in_memory) -> Session:
    Session = sessionmaker(bind=db_in_memory)
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        session.close()
