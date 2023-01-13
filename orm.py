from sqlalchemy import MetaData, Table, Column, Integer, String, Date
from sqlalchemy.orm import registry, relationship

from domain import OrderLine, Batch


metadata = MetaData()
mapper_registry = registry()


order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", String(255)),
    Column("sku", String(256)),
    Column("qty", Integer),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("number", String(255)),
    Column("sku", String(256)),
    Column("qty", Integer),
    Column("eta", Date, nullable=True),
)


def start_mapper():
    # lines_mapper = mapper(OrderLine, order_lines)
    mapper_registry.map_imperatively(OrderLine, order_lines)
    mapper_registry.map_imperatively(Batch, batches)
