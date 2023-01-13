from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from domain import Batch
from repository import BatchRepository


def test_can_save_batch(session: Session):
    row = ("batch-1", "СТОЛ", 10, None)
    batch = Batch(*row)

    repo = BatchRepository(session=session)
    repo.add(batch)
    session.commit()

    rows = list(session.execute(text("SELECT number, sku, qty, eta FROM batches;")))
    assert [row] == rows
