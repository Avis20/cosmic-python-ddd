# src/app/core/product/uow.py

from app.core.common.uow import AbstractUnitOfWork
from app.models.db import session_factory

from app.core.product.repositories import ProductRepository

DEFAULT_SESSION_FACTORY = session_factory


class ProductUnitOfWork(AbstractUnitOfWork):
    repository: ProductRepository

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.repository = ProductRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        # self.session.expunge_all()
        self.session.close()

    def rollback(self):
        # sqlalchemy.orm.exc.DetachedInstanceError: Instance <BatchDomain at 0x7fbf4b17d960> is not bound to a Session; attribute refresh operation cannot proceed
        self.session.expunge_all()
        self.session.rollback()

    def commit(self):
        # self.session.expunge_all()
        self.session.commit()

