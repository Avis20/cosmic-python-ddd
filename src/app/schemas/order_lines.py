
from pydantic import BaseModel

class OrderLineSchema(BaseModel):
    order_id: str
    sku: str
    qty: int