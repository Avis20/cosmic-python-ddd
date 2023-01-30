from typing import Optional, Set, List
from dataclasses import dataclass, field
from datetime import date

from app.core.order_lines.domain import OrderLineDomain
from app.core.batch.exceptions import BatchException


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

    # def __hash__(self):
    #     return hash(self.number)

    def __gt__(self, other):
        if isinstance(other, BatchDomain):
            if self.eta is None:
                return False
            if other.eta is None:
                return True
            return self.eta > other.eta
        return NotImplemented

    def allocate(self, order_line: OrderLineDomain):
        """Размещение товара в партии"""
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def deallocate(self, order_line: OrderLineDomain):
        """Отмена заказа - возвращаем размещенный заказ обратно в партию"""
        if order_line in self._allocations:
            self._allocations.remove(order_line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self.qty - self.allocated_quantity

    def can_allocate(self, order_line: OrderLineDomain):
        return self.sku == order_line.sku and self.available_quantity >= order_line.qty


def allocate(order_line: OrderLineDomain, batches: List[BatchDomain]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
    except StopIteration:
        raise BatchException.OutOfStock

    batch.allocate(order_line)
    return batch.number
