# ./src/app/models/batches.py

from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import registry, relationship

from app.models.db import metadata
from app.core.batch.domain import BatchDomain
from app.models.order_lines import order_line_mapper

mapper_registry = registry()

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("number", String(255)),
    # Column("sku", String(255)),
    Column("sku", ForeignKey("products.sku")),
    Column("qty", Integer),
    Column("eta", Date, nullable=True),
    # Column("product_id", Integer),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("batch_id", Integer, ForeignKey("batches.id"), nullable=False),
    Column("order_line_id", Integer, ForeignKey("order_lines.id"), nullable=False),
)

batch_mapper = mapper_registry.map_imperatively(
    BatchDomain,
    batches,
    properties={
        '_allocations': relationship(
            order_line_mapper, secondary=allocations, collection_class=set
        )
    },
)
