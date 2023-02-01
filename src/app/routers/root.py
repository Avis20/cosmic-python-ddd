from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.models.db import get_session
from app.core.batch.repositories import BatchRepository

from app.core.batch.domain import BatchException

from app.schemas.request.order_lines import OrderLineSchema
from app.schemas.request.batches import BatchAddSchema

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
    try:
        batch_number = services.allocate(
            **order_line.dict(), repository=batch_repository, db_session=db_session
        )
    except (BatchException.OutOfStock, BatchException.InvalidSku) as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": str(error)})

    return {"batch_name": batch_number}


@router.post('/batch/add')
def add_batch(
    batch: BatchAddSchema,
    db_session: Session = Depends(get_session),
):
    batch_repository = BatchRepository(db_session)
    services.add_batch(**batch.dict(), repository=batch_repository, db_session=db_session)
    return {"success": 1}
