
from datetime import date, timedelta
from domain import Batch, OrderLine


def make_batch_and_order_line(sku: str, batch_qty: int, order_line_qty: int):
    """
    Создание партии и товарной позиции
    """
    return (
        Batch("batch-001", sku=sku, qty=batch_qty),
        OrderLine("order_line-001", sku=sku, qty=order_line_qty),
    )


def test_can_allocate_available_greater_the_required():
    """
    Функция проверки возможности добавить заказ в партию
    """
    large_batch, small_order = make_batch_and_order_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_order)


def test_allocate_batch_reduce_available_qty():
    """
    Проверка уменьшения партии на кол-во товаров в заказе
    """
    batch, order_line = make_batch_and_order_line("SMALL-TABLE", 20, 2)

    batch.allocate(order_line)
    assert batch.available_quantity == 18


def test_cannot_allocate_available_greater_the_required():
    small_batch, large_order = make_batch_and_order_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_order) is False


def test_can_allocate_if_available_equals_required():
    batch, order = make_batch_and_order_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(order)


def test_cannot_allocate_if_sku_not_match():
    batch = Batch("batch-001", "BIG-LAMP", 10)
    order_line = OrderLine("order_line-001", "LARGE-TABLE", 10)

    assert batch.can_allocate(order_line) is False


def test_can_only_deallocate_allocated_lines():
    batch, not_allocated_order_line = make_batch_and_order_line("SMALL-TABLE", 20, 2)
    batch.deallocate(not_allocated_order_line)

    assert batch.available_quantity == 20


def test_allocate_is_idempotent():
    batch, order_line = make_batch_and_order_line("TABLE", 20, 2)
    batch.allocate(order_line)
    batch.allocate(order_line)
    assert batch.available_quantity == 18


def test_order_batches_by_eta():
    batch_in_stock = Batch("batch-in-stock", "RETRO-CLOCK", qty=100, eta=date.today())
    tomorrow = date.today() + timedelta(days=1)
    batch_in_shipment = Batch("batch-in-shipment", "RETRO-CLOCK", qty=100, eta=tomorrow)

    batches = sorted([batch_in_shipment, batch_in_stock])
    assert batches[0] == batch_in_stock and batches[1] == batch_in_shipment
