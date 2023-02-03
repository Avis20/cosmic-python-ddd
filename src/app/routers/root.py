from fastapi import APIRouter, HTTPException, status

from app.core.batch.domain import BatchException

from app.core.batch.uow import BatchUnitOfWork

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
):
    uow = BatchUnitOfWork()
    try:
        batch_number = services.allocate(**order_line.dict(), uow=uow)
    except (BatchException.OutOfStock, BatchException.InvalidSku) as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": str(error)})

    return {"batch_name": batch_number}


@router.post('/batch/add')
def add_batch(
    batch: BatchAddSchema,
):
    uow = BatchUnitOfWork()
    services.add_batch(**batch.dict(), uow=uow)
    return {"success": 1}
