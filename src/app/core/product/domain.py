# ./src/app/core/product/domain.py

from typing import List
from dataclasses import dataclass

from app.core.batch.domain import BatchDomain
from app.core.order_lines.domain import OrderLineDomain

from app.core.product.exceptions import ProductExceptions


@dataclass
class ProductDomain:
    sku: str
    batches: List[BatchDomain]

    def allocate(self, order_line: OrderLineDomain) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(order_line))
            batch.allocate(order_line)
            return batch.number
        except StopIteration:
            raise ProductExceptions.OutOfStock("Не найдено подходящей партии товара")
