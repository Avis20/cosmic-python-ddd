from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.models.db import get_session
from app.core.batch.repositories import BatchRepository
from app.core.order_lines.domain import OrderLineDomain

from app.core.batch.domain import BatchException

from app.schemas.request.order_lines import OrderLineSchema

from app.core.batch import services

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Hello Cosmic"}


@router.post('/allocate')
def allocate(
    order_line: OrderLineSchema,
    db_session: Session = Depends(get_session),
):
    batch_repository = BatchRepository(db_session)
    line = OrderLineDomain(**order_line.dict())
    try:
        services.allocate(line, batch_repository, db_session)
    except (BatchException.OutOfStock, BatchException.InvalidSku) as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": str(error)})
