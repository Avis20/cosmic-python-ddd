from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    PrimaryKeyConstraint,
    ForeignKeyConstraint,
)
from app.models.database import BaseModel
from app.models.base import BaseModelMixin


class BatchModel(BaseModel, BaseModelMixin):

    __tablename__ = "batches"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    number = Column("number", String(255))
    sku = Column("sku", String(255))
    qty = Column("qty", Integer)
    eta = Column("eta", Date, nullable=True)


class AllocationsModel(BaseModel):
    __tablename__ = "allocations"
    __table_args__ = (
        PrimaryKeyConstraint(
            "batch_id", "order_line_id", name="batch_order_lines_pkey"
        ),
        ForeignKeyConstraint(["batch_id"], ["batches.id"], name="batch_fkey"),
        ForeignKeyConstraint(
            ["order_line_id"], ["order_lines.id"], name="order_line_fkey"
        ),
    )

    batch_id = Column("batch_id", Integer, nullable=False)
    order_line_id = Column("order_line_id", Integer, nullable=False)
