# src/app/core/common/uow.py

from app.core.common.repositories import AbstractRepository


class AbstractUnitOfWork:
    repository: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def rollback(self):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError
