# ./src/tests/app/domain/test_allocate.py

import pytest
from datetime import date, timedelta


from app.domain.batches import BatchDomain, allocate
from app.domain.orders import OrderLineDomain


def test_current_batch_and_shipment():
    """Проверка размещения товара в партии на складе"""
    tomorrow = date.today() + timedelta(days=1)
    batch_in_stock = BatchDomain("batch-in-stock", "RETRO-CLOCK", qty=100, eta=None)
    batch_in_shipment = BatchDomain(
        "batch-in-shipment", "RETRO-CLOCK", qty=100, eta=tomorrow
    )

    order_line = OrderLineDomain("order-001", "RETRO-CLOCK", qty=10)
    batch_number = allocate(
        batches=[batch_in_stock, batch_in_shipment], order_line=order_line
    )

    assert batch_number == "batch-in-stock"
    assert batch_in_shipment.available_quantity == 100
    assert batch_in_stock.available_quantity == 90


def test_three_batches():
    """Проверка размещения из трех партий товара"""
    today = date.today()
    tomorrow = today + timedelta(days=1)
    later = today + timedelta(days=30)
    early_batch = BatchDomain("fast-batch", "LAMP", qty=100, eta=today)
    medium_batch = BatchDomain("normal-batch", "LAMP", qty=100, eta=tomorrow)
    slow_batch = BatchDomain("slow-batch", "LAMP", qty=100, eta=later)

    order_line = OrderLineDomain("order-001", "LAMP", qty=20)
    batch_number = allocate(
        batches=[early_batch, medium_batch, slow_batch], order_line=order_line
    )

    assert batch_number == early_batch.number
    assert early_batch.available_quantity == 80
    assert slow_batch.available_quantity == 100
    assert medium_batch.available_quantity == 100


@pytest.mark.skip()
def test_raises_of_stock():
    batch = BatchDomain("batch1", "SMALL-FORK", 10, eta=date.today())
    order_line = OrderLineDomain("order-001", "SMALL-FORK", qty=10)
    # product = ProductDomain("SMALL-FORK", batches=[batch])

    allocate(batches=[batch], order_line=order_line)

    # with pytest.raises(ProductExceptions.OutOfStock):
    #     product.allocate(order_line)
