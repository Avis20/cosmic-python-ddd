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
    version_number: int = 0

    def get_batch(self, sku):
        batch = next((p for p in self.batches if p.sku == sku), None)
        print('\n\n')
        print(repr(batch))
        print('allocated_quantity', batch.allocated_quantity)
        print('available_quantity', batch.available_quantity)
        print('\n\n')
        return batch

    def allocate(self, order_line: OrderLineDomain) -> str:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(order_line))
            batch.allocate(order_line)
            self.version_number += 1
            return batch.number
        except StopIteration:
            raise ProductExceptions.OutOfStock("Не найдено подходящей партии товара")
