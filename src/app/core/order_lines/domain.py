from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class OrderLineDomain:
    order_id: str
    sku: str
    qty: int
