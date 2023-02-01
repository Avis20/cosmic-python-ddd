from typing import List
from sqlalchemy.orm import Session

from app.core.order_lines.domain import OrderLineDomain
from app.core.common.repositories import AbstractRepository

from app.core.batch.exceptions import BatchException
from app.core.batch.domain import BatchDomain, allocate as batch_allocate
from app.core.batch.repositories import BatchRepository


def is_valid_sku(sku: str, batches: List[BatchDomain]):
    return sku in {batch.sku for batch in batches}


def allocate(line: OrderLineDomain, repository: BatchRepository, db_session: Session):
    batches = repository.list()
    if not is_valid_sku(line.sku, batches):
        raise BatchException.InvalidSku(f"Недопустимый артикул {line.sku}")
    batch_number = batch_allocate(line, batches)
    db_session.commit()
    return batch_number


def add_batch(batch: BatchDomain, repository: BatchRepository, db_session: Session):
    db_session.begin()
    repository.add(batch)
    db_session.commit()


def deallocate(
    line: OrderLineDomain, batch: BatchDomain, repository: BatchRepository, db_session: Session
):
    if line.sku != batch.sku:
        raise BatchException.InvalidSku(f"Недопустимый артикул {line.sku}")
    batch.deallocate(line)
    db_session.commit()
