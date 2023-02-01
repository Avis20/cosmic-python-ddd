from typing import List
from sqlalchemy.orm import Session

from app.core.common.repositories import AbstractRepository
from app.core.batch.domain import BatchDomain

class FakeBatchRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = batches

    def add(self, batch):
        return self._batches.append(batch)

    def get(self, number):
        return next(batch for batch in self._batches if batch.number == number)

    def list(self):
        return list(self._batches)


class BatchRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, instance: BatchDomain):
        self.session.add(instance)

    def get(self, number: str) -> BatchDomain | None:
        # select возвращает "sqlalchemy.engine.row.Row"
        # а query возвращает "domain.Batch"
        # stmt = select(Batch).filter_by(number=number)
        # row = self.session.execute(stmt).fetchone()
        return self.session.query(BatchDomain).filter_by(number=number).one()

    def list(self) -> List[BatchDomain]:
        return self.session.query(BatchDomain).all()
