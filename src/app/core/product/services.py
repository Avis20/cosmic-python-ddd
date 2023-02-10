# ./src/app/core/product/services.py

from typing import Optional
from datetime import date

from app.core.product.uow import ProductUnitOfWork
from app.core.product.domain import ProductDomain
from app.core.product.exceptions import ProductExceptions

from app.core.batch.domain import BatchDomain
from app.core.order_lines.domain import OrderLineDomain


class ProductService:
    def add_batch(
        self, number: str, sku: str, qty: int, eta: Optional[date], uow: ProductUnitOfWork
    ):
        """Добавление партии продукта"""
        batch = BatchDomain(number, sku, qty, eta)
        with uow:
            product = uow.repository.get(sku)
            if not product:
                product = ProductDomain(sku, batches=[])
                uow.repository.add(product)
            product.batches.append(batch)
            uow.commit()

    def allocate(self, order_id: str, sku: str, qty: int, uow: ProductUnitOfWork) -> str:
        """Регистрация нового товара"""
        line = OrderLineDomain(order_id, sku, qty)
        with uow:
            product = uow.repository.get(sku)
            if not product:
                raise ProductExceptions.InvalidSku(f"Недопустимый артикул {sku}")
            batch_number = product.allocate(line)
            uow.commit()
        return batch_number
