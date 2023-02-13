# ./src/app/core/product/repositories.py

from sqlalchemy.orm import Session

from app.core.common.repositories import AbstractRepository
from app.core.product.domain import ProductDomain


class ProductRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, product: ProductDomain):
        self.session.add(product)

    def get(self, sku: str) -> ProductDomain | None:
        return self.session.query(ProductDomain).filter_by(sku=sku).with_for_update().first()
