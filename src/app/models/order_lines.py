# ./src/app/models/order_lines.py

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry

from app.models.db import metadata
from app.core.order_lines.domain import OrderLineDomain

mapper_registry = registry()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String(255)),
    Column("sku", String(256)),
    Column("qty", Integer),
)

order_line_mapper = mapper_registry.map_imperatively(OrderLineDomain, order_lines)
