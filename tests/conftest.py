import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from orm import metadata, start_mapper


@pytest.fixture
def db_in_memory():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(db_in_memory) -> Session:
    # assert 1 == 2
    start_mapper()
    Session = sessionmaker(bind=db_in_memory)
    session = Session()
    try:
        yield session
    finally:
        clear_mappers()
        session.close()
