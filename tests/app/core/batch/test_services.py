import pytest
from datetime import date, timedelta

from app.core.order_lines.domain import OrderLineDomain
from app.core.batch.domain import BatchDomain
from app.core.batch.repositories import FakeBatchRepository
from app.core.batch import services
from app.core.batch.exceptions import BatchException


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True

    def begin(self):
        print("SESSION begin:")


def test_allocations():
    line = OrderLineDomain("o1", "СТОЛ", 10)

    today = date.today()
    tomorrow = today + timedelta(days=1)

    batch1 = BatchDomain("b1", "СТОЛ", 10, today)
    batch2 = BatchDomain("b2", "СТОЛ", 100, tomorrow)

    fake_repo = FakeBatchRepository([batch1, batch2])
    fake_session = FakeSession()

    batch_name = services.allocate(line, repository=fake_repo, db_session=fake_session)
    assert batch_name == "b1"


def test_invalid_sku():
    line = OrderLineDomain("o1", "СТОЛ", 10)
    batch1 = BatchDomain("b1", "СТУЛ", 10)
    fake_repo = FakeBatchRepository([batch1])
    fake_session = FakeSession()

    with pytest.raises(BatchException.InvalidSku, match=f"Недопустимый артикул СТОЛ"):
        services.allocate(line, repository=fake_repo, db_session=fake_session)


def test_deallocate():
    line = OrderLineDomain("o1", "СТОЛ", 10)
    batch = BatchDomain("b1", "СТОЛ", 100)
    fake_repo, fake_session = FakeBatchRepository([]), FakeSession()
    services.add_batch(batch, repository=fake_repo, db_session=fake_session)

    batch_name = services.allocate(line, repository=fake_repo, db_session=fake_session)
    assert batch_name == "b1"
    assert batch.available_quantity == 90

    services.deallocate(line, batch, fake_repo, fake_session)
    assert batch.available_quantity == 100


def test_deallocate_valid_sku():
    line1 = OrderLineDomain("o1", "СТОЛ", 10)
    line2 = OrderLineDomain("o2", "СТУЛ", 10)

    batch = BatchDomain("b1", "СТОЛ", 100)
    fake_repo = FakeBatchRepository([batch])
    fake_session = FakeSession()

    batch_name = services.allocate(line1, repository=fake_repo, db_session=fake_session)
    assert batch_name == "b1"
    assert batch.available_quantity == 90

    with pytest.raises(BatchException.InvalidSku, match=f"Недопустимый артикул СТУЛ"):
        services.deallocate(line2, batch, fake_repo, fake_session)
    assert batch.available_quantity == 90

