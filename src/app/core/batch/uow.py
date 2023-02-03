# src/app/core/batch/uow.py

from app.core.common.uow import AbstractUnitOfWork
from app.models.db import session_factory

from app.core.batch.repositories import BatchRepository

DEFAULT_SESSION_FACTORY = session_factory


class BatchUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.repository = BatchRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()
