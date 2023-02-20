# ./src/app/repository/batches.py

from sqlalchemy.orm import Session

from app.repository.abstract import AbstractRepository
from app.domain.batches import BatchDomain
from app.models.batches import BatchModel


class BatchRepository(AbstractRepository):

    model = BatchModel

    def __init__(self, session: Session):
        self.session = session

    def add(self, batch: BatchDomain) -> BatchDomain:
        batch_orm = BatchModel.from_domain(batch)
        self.session.add(batch_orm)
