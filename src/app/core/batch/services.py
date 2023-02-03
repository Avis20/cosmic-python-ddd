from typing import List
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.core.order_lines.domain import OrderLineDomain

from app.core.batch.exceptions import BatchException
from app.core.batch.domain import BatchDomain, allocate as batch_allocate
from app.core.batch.repositories import BatchRepository
from app.core.batch.uow import BatchUnitOfWork

from app.core.common.uow import AbstractUnitOfWork


def is_valid_sku(sku: str, batches: List[BatchDomain]):
    return sku in {batch.sku for batch in batches}


def allocate(order_id: str, sku: str, qty: int, uow: BatchUnitOfWork) -> str:
    line = OrderLineDomain(order_id, sku, qty)
    with uow:
        batches = uow.repository.list()
        if not is_valid_sku(line.sku, batches):
            raise BatchException.InvalidSku(f"Недопустимый артикул {line.sku}")
        batch_number = batch_allocate(line, batches)
        uow.commit()
    return batch_number


def add_batch(
    number: str, sku: str, qty: int, eta: Optional[date], uow: BatchUnitOfWork
) -> BatchDomain:
    with uow:
        batch = BatchDomain(number, sku, qty, eta)
        uow.repository.add(batch)
        uow.commit()
    return batch


def deallocate(order_id: str, sku: str, qty: int, batch: BatchDomain, uow: BatchUnitOfWork):
    with uow:
        line = OrderLineDomain(order_id, sku, qty)
        if line.sku != batch.sku:
            raise BatchException.InvalidSku(f"Недопустимый артикул {line.sku}")
        batch.deallocate(line)
        uow.commit()
