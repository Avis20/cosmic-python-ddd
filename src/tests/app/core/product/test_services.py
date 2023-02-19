# ./tests/app/core/product/test_services.py

import pytest
from datetime import date, timedelta

from app.core.common.repositories import AbstractRepository
from app.core.common.uow import AbstractUnitOfWork
from app.core.product.services import ProductService
from app.core.product.exceptions import ProductExceptions


class FakeProductRepository(AbstractRepository):
    def __init__(self, products):
        self._products = list(products)

    def add(self, product):
        self._products.append(product)

    def get(self, sku):
        return next((p for p in self._products if p.sku == sku), None)

    def list(self):
        return list(self._products)


class FakeProductUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.repository = FakeProductRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_batch():
    """Проверка сервиса товаров по добавлению новой партии"""
    uow = FakeProductUnitOfWork()
    product_service = ProductService()
    product_service.add_batch("b1", "СТОЛ", 10, None, uow=uow)
    assert uow.repository.get("СТОЛ") is not None
    assert uow.committed


def test_allocations():
    """Проверка сервиса по размещению товарной позиции в партию"""
    line = ["o1", "СТОЛ", 10]

    today = date.today()
    tomorrow = today + timedelta(days=1)

    batch1 = dict(number="b1", sku="СТОЛ", qty=100, eta=today)
    batch2 = dict(number="b2", sku="СТОЛ", qty=100, eta=tomorrow)
    uow = FakeProductUnitOfWork()
    product_service = ProductService()
    product_service.add_batch(**batch2, uow=uow)
    product_service.add_batch(**batch1, uow=uow)

    batch_name = product_service.allocate(*line, uow=uow)
    assert uow.committed
    assert batch_name == "b1"


def test_invalid_sku():
    """Проверка вызова недопустимого sku"""
    line = ["o1", "СТОЛ", 10]

    uow = FakeProductUnitOfWork()
    product_service = ProductService()
    product_service.add_batch(number="b1", sku="СТУЛ", qty=100, eta=None, uow=uow)

    with pytest.raises(ProductExceptions.InvalidSku, match=f"Недопустимый артикул СТОЛ"):
        product_service.allocate(*line, uow=uow)
