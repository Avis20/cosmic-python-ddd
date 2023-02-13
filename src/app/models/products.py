# ./src/app/models/products.py

from sqlalchemy import Table, Column, String, Integer
from sqlalchemy.orm import registry, relationship

from app.core.product.domain import ProductDomain
from app.models.db import metadata
from app.models.batches import batch_mapper

mapper_registry = registry()

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(256)),
    Column("version_number", Integer, nullable=False, server_default="0"),
)

product_mapper = mapper_registry.map_imperatively(
    # ProductDomain, products, properties={"batches": relationship(batch_mapper, lazy='noload')}, 
    ProductDomain, products, properties={"batches": relationship(batch_mapper, lazy='select')}, 
    # ProductDomain, products, properties={"batches": relationship(batch_mapper)}, 
)
