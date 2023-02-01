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
    line = ["o1", "СТОЛ", 10]

    today = date.today()
    tomorrow = today + timedelta(days=1)

    fake_repo = FakeBatchRepository([])
    fake_session = FakeSession()
    batch1 = dict(number="b1", sku="СТОЛ", qty=100, eta=today)
    batch2 = dict(number="b2", sku="СТОЛ", qty=100, eta=tomorrow)
    services.add_batch(**batch2, repository=fake_repo, db_session=fake_session)
    services.add_batch(**batch1, repository=fake_repo, db_session=fake_session)

    batch_name = services.allocate(*line, repository=fake_repo, db_session=fake_session)
    assert batch_name == "b1"


def test_invalid_sku():
    line = ["o1", "СТОЛ", 10]
    fake_repo = FakeBatchRepository([])
    fake_session = FakeSession()
    services.add_batch(
        number="b1", sku="СТУЛ", qty=100, repository=fake_repo, db_session=fake_session
    )

    with pytest.raises(BatchException.InvalidSku, match=f"Недопустимый артикул СТОЛ"):
        services.allocate(*line, repository=fake_repo, db_session=fake_session)


def test_deallocate():
    line = ["o1", "СТОЛ", 10]
    fake_repo, fake_session = FakeBatchRepository([]), FakeSession()
    batch = services.add_batch(
        number="b1", sku="СТОЛ", qty=100, repository=fake_repo, db_session=fake_session
    )

    batch_name = services.allocate(*line, repository=fake_repo, db_session=fake_session)
    assert batch_name == "b1"
    assert batch.available_quantity == 90

    services.deallocate(*line, batch, repository=fake_repo, db_session=fake_session)
    assert batch.available_quantity == 100


def test_deallocate_valid_sku():
    line1 = ["o1", "СТОЛ", 10]
    line2 = ["o2", "СТУЛ", 10]

    fake_repo = FakeBatchRepository([])
    fake_session = FakeSession()
    services.add_batch(
        number="b1", sku="СТОЛ", qty=100, repository=fake_repo, db_session=fake_session
    )

    batch_name = services.allocate(*line1, repository=fake_repo, db_session=fake_session)
    batch = fake_repo.get("b1")
    assert batch_name == "b1"
    assert batch.available_quantity == 90

    with pytest.raises(BatchException.InvalidSku, match=f"Недопустимый артикул СТУЛ"):
        services.deallocate(*line2, batch, fake_repo, fake_session)
    assert batch.available_quantity == 90
