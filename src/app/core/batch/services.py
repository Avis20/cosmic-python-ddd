from typing import List, Optional
from datetime import date

from app.core.order_lines.domain import OrderLineDomain

from app.core.batch.exceptions import BatchException
from app.core.batch.domain import BatchDomain
from app.core.batch.uow import BatchUnitOfWork


class BatchService:
    def is_valid_sku(self, sku: str, batches: List[BatchDomain]):
        """Проверка есть ли среди партий переданный sku
        sku - единица складского учета (артикул)
        """
        return sku in {batch.sku for batch in batches}

    def add_batch(
        self, number: str, sku: str, qty: int, eta: Optional[date], uow: BatchUnitOfWork
    ) -> BatchDomain:
        """Создание партии товара"""
        with uow:
            batch = BatchDomain(number, sku, qty, eta)
            uow.repository.add(batch)
            uow.commit()
        return batch

    def deallocate(
        self, order_id: str, sku: str, qty: int, batch: BatchDomain, uow: BatchUnitOfWork
    ):
        """Отмена регистрации товара"""
        with uow:
            line = OrderLineDomain(order_id, sku, qty)
            if line.sku != batch.sku:
                raise BatchException.InvalidSku(f"Недопустимый артикул {line.sku}")
            batch.deallocate(line)
            uow.commit()
