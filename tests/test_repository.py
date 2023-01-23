from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.domain import Batch, OrderLine
from app.repository import BatchRepository


def test_can_save_batch(session: Session):
    row = ("batch-1", "СТОЛ", 10, None)
    batch = Batch(*row)

    repo = BatchRepository(session=session)
    repo.add(batch)
    session.commit()

    rows = list(session.execute(text("SELECT number, sku, qty, eta FROM batches;")))
    assert [row] == rows


def insert_order_line(session: Session, order_number: str) -> int | None:
    order_line_id = session.execute(
        text(
            "INSERT INTO order_lines (order_id, sku, qty) VALUES "
            f'("{order_number}", "SOME", 2)'
            "RETURNING id"
        )
    ).scalar()
    return order_line_id


def insert_batch(session: Session, number: str) -> int | None:
    batch_id = session.execute(
        text(
            "INSERT INTO batches (number, sku, qty) VALUES "
            f'(("{number}"), "SOME", 10) '
            "RETURNING id"
        )
    ).scalar()
    return batch_id


def insert_allocation(session: Session, batch_id: int, order_line_id: int):
    session.execute(
        text(
            "INSERT INTO allocations (batch_id, order_line_id) VALUES "
            f'("{batch_id}", "{order_line_id}")'
        )
    )


def test_can_retrieve_bath_with_allocation(session: Session):
    batch_id = insert_batch(session, "batch-1")
    order_line_id = insert_order_line(session, "order-1")
    insert_batch(session, "batch-2")

    if not batch_id or not order_line_id:
        raise Exception("Not Found")
    insert_allocation(session, batch_id, order_line_id)

    batch_repo = BatchRepository(session)
    batch_in_db = batch_repo.get("batch-1")

    if not batch_in_db:
        raise Exception("Not Found")

    expected_batch = Batch("batch-1", "SOME", 10)

    # Сравниваются только number
    assert batch_in_db == expected_batch

    assert batch_in_db.sku == expected_batch.sku
    assert batch_in_db.eta == expected_batch.eta
    assert batch_in_db._allocations == {OrderLine("order-1", "SOME", 2)}
