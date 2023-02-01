from typing import Optional
from pydantic import BaseModel
from datetime import date


class BatchAddSchema(BaseModel):
    number: str
    sku: str
    qty: int
    eta: Optional[date]
