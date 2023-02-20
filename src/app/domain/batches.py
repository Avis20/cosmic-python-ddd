# ./src/app/domain/batches.py

from typing import Optional, Set, List
from datetime import date
from dataclasses import dataclass, field

from app.domain.orders import OrderLineDomain


@dataclass
class BatchDomain:
    # number - порядковый номер партии
    number: str
    # sku - единица складского учета (артикул)
    sku: str
    # qty - кол-во товаров в партии
    qty: int = 0
    # eta - предполагаемый срок прибытия
    eta: Optional[date] = None
    # словарь товарных позиций
    _allocations: Set[OrderLineDomain] = field(default_factory=set)

    def __eq__(self, other):
        if isinstance(other, BatchDomain):
            return self.number == other.number
        return NotImplemented

    def __hash__(self):
        return hash(self.number)

    def __gt__(self, other):
        if isinstance(other, BatchDomain):
            if self.eta is None:
                return False
            if other.eta is None:
                return True
            return self.eta > other.eta
        return NotImplemented

    def allocate(self, order_line: OrderLineDomain):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def deallocate(self, order_line: OrderLineDomain):
        if order_line in self._allocations:
            self._allocations.remove(order_line)

    def can_allocate(self, order_line: OrderLineDomain) -> bool:
        return self.sku == order_line.sku and self.qty >= order_line.qty

    @property
    def allocated_quantity(self):
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self):
        return self.qty - self.allocated_quantity


def allocate(batches: List[BatchDomain], order_line: OrderLineDomain) -> str:
    batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
    batch.allocate(order_line)
    return batch.number
