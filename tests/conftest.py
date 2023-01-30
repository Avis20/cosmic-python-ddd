import pytest
from sqlalchemy.orm import Session, sessionmaker, clear_mappers
from sqlalchemy import create_engine

import app.models.base
from app.models.db import metadata
from app.settings import get_settings

settings = get_settings()

@pytest.fixture()
def db_in_memory():
    engine = create_engine("sqlite:///:memory:")
    # Для test_api
    # engine = create_engine(settings.get_postgres_uri)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(db_in_memory) -> Session:
    Session = sessionmaker(bind=db_in_memory)
    session = Session()
    try:
        yield session
        session.commit()
    finally:
        # clear_mappers()
        session.close()


@pytest.fixture
def add_stock(session: Session):
    batches = set()
    order_lines = set()

    def _add_stock(lines):
        for batch, sku, qty, eta in lines:
            [[batch_id]] = session.execute(
                'INSERT INTO batches ("number", "sku", "qty", "eta") '
                'VALUES (:number, :sku, :qty, :eta) RETURNING id',
                dict(number=batch, sku=sku, qty=qty, eta=eta)
            )
            batches.add(batch_id)
        session.commit()

    yield _add_stock

    print('\n\n')
    print('CLEAN')
    print('\n\n')

    for batch_id in batches:
        session.execute(
            'DELETE FROM allocations WHERE batch_id = :batch_id', dict(batch_id=batch_id)
        )
        session.execute(
            'DELETE FROM batches WHERE id = :batch_id', dict(batch_id=batch_id)
        )
