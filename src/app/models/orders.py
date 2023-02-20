from sqlalchemy import Column, Integer, String

from app.models.database import BaseModel
from app.models.base import BaseModelMixin


class OrderLineModel(BaseModel, BaseModelMixin):

    __tablename__ = "order_lines"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    sku = Column("sku", String(256))
    qty = Column("qty", Integer)
