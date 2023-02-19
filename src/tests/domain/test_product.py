import pytest
from datetime import date, timedelta

from app.core.batch.exceptions import BatchException
from app.core.batch.domain import BatchDomain
from app.core.order_lines.domain import OrderLineDomain

from app.core.product.domain import ProductDomain
from app.core.product.exceptions import ProductExceptions


def test_current_batch_and_shipment():
    """Проверка аллокации товара в партии на складе"""
    tomorrow = date.today() + timedelta(days=1)
    batch_in_stock = BatchDomain("batch-in-stock", "RETRO-CLOCK", qty=100, eta=None)
    batch_in_shipment = BatchDomain("batch-in-shipment", "RETRO-CLOCK", qty=100, eta=tomorrow)
    product = ProductDomain("RETRO-CLOCK", batches=[batch_in_stock, batch_in_shipment])

    order_line = OrderLineDomain("order-001", "RETRO-CLOCK", qty=10)
    batch_name = product.allocate(order_line)

    assert batch_name == "batch-in-stock"
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
    product = ProductDomain("LAMP", batches=[slow_batch, medium_batch, early_batch])

    order_line = OrderLineDomain("order-001", "LAMP", qty=20)
    batch_name = product.allocate(order_line)

    assert batch_name == early_batch.number
    assert early_batch.available_quantity == 80
    assert slow_batch.available_quantity == 100
    assert medium_batch.available_quantity == 100


def test_raises_of_stock():
    batch = BatchDomain("batch1", "SMALL-FORK", 10, eta=date.today())
    order_line = OrderLineDomain("order-001", "SMALL-FORK", qty=10)
    product = ProductDomain("SMALL-FORK", batches=[batch])

    product.allocate(order_line)

    with pytest.raises(ProductExceptions.OutOfStock):
        product.allocate(order_line)
