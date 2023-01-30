from typing import List
from sqlalchemy.orm import Session

from app.core.order_lines.domain import OrderLineDomain
from app.core.common.repositories import BaseRepository

from app.core.batch.exceptions import BatchException
from app.core.batch.domain import BatchDomain


def is_valid_sku(sku: str, batches: List[BatchDomain]):
    return sku in {batch.sku for batch in batches}


def allocate(line: OrderLineDomain, repository: BaseRepository, db_session: Session):
    batches = repository.list()
    if not is_valid_sku(line.sku, batches):
        raise BatchException.InvalidSku(f"Недопустимый артикул {line.sku}")
