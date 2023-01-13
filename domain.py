# batches_domain.py

from typing import Optional, Set, List
from datetime import date
from dataclasses import dataclass, field


# @dataclass(frozen=True)
@dataclass(unsafe_hash=True)
class OrderLine:
    order_id: str
    sku: str
    qty: int


@dataclass
class Batch:
    # number - порядковый номер партии
    number: str
    # sku - единица складского учета (артикул)
    sku: str
    # qty - кол-во товаров в партии
    qty: int = 0
    # eta - предполагаемый срок прибытия
    eta: Optional[date] = None
    # словарь товарных позиций
    _allocated_order_lines: Set[OrderLine] = field(default_factory=set)

    def __gt__(self, other):
        if isinstance(other, Batch):
            if self.eta is None:
                return False
            if other.eta is None:
                return True
            return self.eta > other.eta
        return NotImplemented

    def allocate(self, order_line: OrderLine):
        """Размещение товара в партии"""
        if self.can_allocate(order_line):
            self._allocated_order_lines.add(order_line)

    def deallocate(self, order_line: OrderLine):
        """Отмена заказа - возвращаем размещенный заказ обратно в партию"""
        if order_line in self._allocated_order_lines:
            self._allocated_order_lines.remove(order_line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocated_order_lines)

    @property
    def available_quantity(self) -> int:
        return self.qty - self.allocated_quantity

    def can_allocate(self, order_line: OrderLine):
        return self.sku == order_line.sku and self.available_quantity >= order_line.qty


class OutOfStock(Exception):
    pass


def allocate(order_line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
    except StopIteration:
        raise OutOfStock

    batch.allocate(order_line)
    return batch.number
