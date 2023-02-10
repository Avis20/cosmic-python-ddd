# ./src/app/routers/root.py

from fastapi import APIRouter, HTTPException, status

from app.schemas.request.order_lines import OrderLineSchema
from app.schemas.request.batches import BatchAddSchema

from app.core.product.services import ProductService
from app.core.product.uow import ProductUnitOfWork
from app.core.product.exceptions import ProductExceptions

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Hello Cosmic"}


@router.post('/allocate')
def allocate(
    order_line: OrderLineSchema,
):
    uow = ProductUnitOfWork()
    try:
        product_service = ProductService()
        batch_number = product_service.allocate(**order_line.dict(), uow=uow)
    except (ProductExceptions.OutOfStock, ProductExceptions.InvalidSku) as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail={"error": str(error)})

    return {"batch_name": batch_number}


@router.post('/batch/add')
def add_batch(
    batch: BatchAddSchema,
):
    uow = ProductUnitOfWork()
    product_service = ProductService()
    product_service.add_batch(**batch.dict(), uow=uow)
    return {"success": 1}
