from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.models.db import get_session
from app.repository import BatchRepository

import domain

from app.schemas.order_lines import OrderLineSchema

router = APIRouter()


@router.get("/")
def root():
    return "Hello Cosmic"


@router.post('/allocate')
def allocate(
    order_line: OrderLineSchema,
    db_session: Session = Depends(get_session),
):
    batches = BatchRepository(db_session).list()
    line = domain.OrderLine(**order_line.dict())

    batch = domain.allocate(order_line=line, batches=batches)
    print(batch)

    return 1
