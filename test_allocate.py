import pytest
from datetime import date, timedelta

from batches_domain import Batch, OrderLine, allocate, OutOfStock


def test_current_batch_and_shipment():
    batch_in_stock = Batch("batch-in-stock", "RETRO-CLOCK", qty=100, eta=None)
    tomorrow = date.today() + timedelta(days=1)
    batch_in_shipment = Batch("batch-in-shipment", "RETRO-CLOCK", qty=100, eta=tomorrow)

    order_line = OrderLine("order-001", "RETRO-CLOCK", qty=10)
    allocate(order_line=order_line, batches=[batch_in_shipment, batch_in_stock])

    assert batch_in_shipment.available_quantity == 100
    assert batch_in_stock.available_quantity == 90


def test_three_batches():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    later = today + timedelta(days=30)
    early_batch = Batch("fast-batch", "LAMP", qty=100, eta=today)
    medium_batch = Batch("normal-batch", "LAMP", qty=100, eta=tomorrow)
    slow_batch = Batch("normal-batch", "LAMP", qty=100, eta=later)

    order_line = OrderLine("order-001", "LAMP", qty=20)

    allocate(order_line, [early_batch, medium_batch, slow_batch])
    assert early_batch.available_quantity == 80
    assert slow_batch.available_quantity == 100
    assert medium_batch.available_quantity == 100


def test_return_allocated_batch():
    batch_in_stock = Batch("batch-in-stock", "RETRO-CLOCK", qty=100, eta=None)
    tomorrow = date.today() + timedelta(days=1)
    batch_in_shipment = Batch("batch-in-shipment", "RETRO-CLOCK", qty=100, eta=tomorrow)

    order_line = OrderLine("order-001", "RETRO-CLOCK", qty=10)
    allocated = allocate(
        order_line=order_line, batches=[batch_in_shipment, batch_in_stock]
    )

    assert allocated == batch_in_stock.number


def test_raises_of_stock():
    batch = Batch("batch1", "SMALL-FORK", 10, eta=date.today())
    order_line = OrderLine("order-001", "SMALL-FORK", qty=10)

    allocate(order_line, [batch])

    with pytest.raises(OutOfStock):
        allocate(order_line, [batch])
