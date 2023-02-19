# ./tests/app/core/batch/test_uow.py

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.core.batch.uow import BatchUnitOfWork


def insert_batch(session: Session, number, sku, qty, eta):
    session.execute(
        text("INSERT INTO batches (number, sku, qty, eta) VALUES" "(:number, :sku, :qty, :eta)"),
        dict(number=number, sku=sku, qty=qty, eta=eta),
    )


def test_rollback_if_not_commit(session_factory):
    """Проверяем что без явного commit через uow в БД ничего не попадет"""
    uow = BatchUnitOfWork(session_factory)
    with uow:
        insert_batch(uow.session, "batch-1", "СТОЛ", 20, None)
        # uow.commit() Если будет commit то запись сохранится

    new_session = session_factory()
    batches = new_session.execute(text("SELECT * FROM batches")).fetchall()
    assert batches == []


def test_rollback_on_error(session_factory):
    """Проверяем что при except также ничего в БД не попадет"""

    class MyExcept(Exception):
        pass

    uow = BatchUnitOfWork(session_factory)
    with pytest.raises(MyExcept):
        with uow:
            insert_batch(uow.session, "batch-1", "СТОЛ", 20, None)
            # uow.commit() Если будет commit то запись сохранится
            raise MyExcept("Some error")

    new_session = session_factory()
    batches = new_session.execute(text("SELECT * FROM batches")).fetchall()
    assert batches == []
