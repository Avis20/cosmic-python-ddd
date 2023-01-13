from abc import ABC
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from domain import Batch

class BaseRepository(ABC):
    def add(self):
        raise NotImplementedError


class BatchRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, instance: Batch):
        self.session.add(instance)
