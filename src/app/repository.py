from abc import ABC
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.app.domain import Batch


class BaseRepository(ABC):
    def add(self):
        raise NotImplementedError

    def get(self, reference: Any):
        raise NotImplementedError


class FakeBatchRepository(BaseRepository):
    def __init__(self, batches):
        self._batches = batches

    def add(self, batch):
        return self._batches.add(batch)

    def get(self, number):
        return next(batch for batch in self._batches if batch.number == number)

    # def list


class BatchRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, instance: Batch):
        self.session.add(instance)

    def get(self, number: str) -> Batch | None:
        # select возвращает "sqlalchemy.engine.row.Row"
        # а query возвращает "domain.Batch"
        # stmt = select(Batch).filter_by(number=number)
        # row = self.session.execute(stmt).fetchone()
        return self.session.query(Batch).filter_by(number=number).one()
