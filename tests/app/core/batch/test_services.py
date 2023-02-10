
# ./tests/app/core/batch/test_services.py

import pytest
from datetime import date, timedelta

from app.core.common.repositories import AbstractRepository
from app.core.common.uow import AbstractUnitOfWork
from app.core.batch.services import BatchService
from app.core.batch.exceptions import BatchException


class FakeBatchRepository(AbstractRepository):
    def __init__(self, batches):
        self._batches = batches

    def add(self, batch):
        return self._batches.append(batch)

    def get(self, number):
        return next(batch for batch in self._batches if batch.number == number)

    def list(self):
        return list(self._batches)


class FakeBatchUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        self.repository = FakeBatchRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_batch():
    """Проверка сервиса с добавлением партии с использованием fake uow"""
    uow = FakeBatchUnitOfWork()
    batch_service = BatchService()
    batch_service.add_batch("b1", "СТОЛ", 10, None, uow=uow)
    assert uow.repository.get("b1") is not None
    assert uow.committed


def test_allocations():
    """Проверка сервиса с алокацией патрии"""
    line = ["o1", "СТОЛ", 10]

    today = date.today()
    tomorrow = today + timedelta(days=1)

    batch1 = dict(number="b1", sku="СТОЛ", qty=100, eta=today)
    batch2 = dict(number="b2", sku="СТОЛ", qty=100, eta=tomorrow)
    uow = FakeBatchUnitOfWork()
    batch_service = BatchService()
    batch_service.add_batch(**batch2, uow=uow)
    batch_service.add_batch(**batch1, uow=uow)

    batch_name = batch_service.allocate(*line, uow=uow)
    assert batch_name == "b1"


def test_invalid_sku():
    """Проверка вызова недопустимого sku"""
    line = ["o1", "СТОЛ", 10]

    uow = FakeBatchUnitOfWork()
    batch_service = BatchService()
    batch_service.add_batch(number="b1", sku="СТУЛ", qty=100, eta=None, uow=uow)

    with pytest.raises(BatchException.InvalidSku, match=f"Недопустимый артикул СТОЛ"):
        batch_service.allocate(*line, uow=uow)


def test_deallocate():
    """алокация и деалокация товара из партии"""
    line = ["o1", "СТОЛ", 10]
    uow = FakeBatchUnitOfWork()
    batch_service = BatchService()
    batch = batch_service.add_batch(number="b1", sku="СТОЛ", qty=100, eta=None, uow=uow)

    batch_name = batch_service.allocate(*line, uow=uow)
    assert batch_name == "b1"
    assert batch.available_quantity == 90

    batch_service.deallocate(*line, batch, uow=uow)
    assert batch.available_quantity == 100


def test_deallocate_valid_sku():
    """Проверка деалокации недопустимого sku"""
    line1 = ["o1", "СТОЛ", 10]
    line2 = ["o2", "СТУЛ", 10]

    uow = FakeBatchUnitOfWork()
    batch_service = BatchService()
    batch_service.add_batch(number="b1", sku="СТОЛ", qty=100, eta=None, uow=uow)

    batch_name = batch_service.allocate(*line1, uow=uow)
    batch = uow.repository.get("b1")
    assert batch_name == "b1"
    assert batch.available_quantity == 90

    with pytest.raises(BatchException.InvalidSku, match=f"Недопустимый артикул СТУЛ"):
        batch_service.deallocate(*line2, batch, uow=uow)
    assert batch.available_quantity == 90
