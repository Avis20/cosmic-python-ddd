from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import registry, relationship

from src.app.domain import OrderLine, Batch


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

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("batch_id", Integer, ForeignKey("batches.id"), nullable=False),
    Column("order_line_id", Integer, ForeignKey("order_lines.id"), nullable=False),
)


def start_mapper():
    # lines_mapper = mapper(OrderLine, order_lines)
    order_line_mapper = mapper_registry.map_imperatively(OrderLine, order_lines)
    mapper_registry.map_imperatively(
        Batch,
        batches,
        properties={
            '_allocations': relationship(
                order_line_mapper, secondary=allocations, collection_class=set
            )
        }
    )
