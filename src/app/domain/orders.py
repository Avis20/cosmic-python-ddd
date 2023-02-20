# ./src/app/domain/orders.py

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLineDomain:
    id: str
    sku: str
    qty: int
