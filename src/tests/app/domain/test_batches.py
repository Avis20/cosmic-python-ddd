# ./src/tests/app/domain/test_batches.py

from app.domain.batches import BatchDomain
from app.domain.orders import OrderLineDomain


def make_batch_and_order_line(sku: str, batch_qty: int, order_line_qty: int):
    """Создание партии и товарной позиции"""
    return (
        BatchDomain("batch-001", sku=sku, qty=batch_qty),
        OrderLineDomain("order_line-001", sku=sku, qty=order_line_qty),
    )


class TestCanAllocate:
    def test_can_allocate_available_greater_the_required(self):
        """Функция проверки возможности добавить заказ в партию"""
        large_batch, small_order = make_batch_and_order_line("СТОЛ", 20, 2)
        assert large_batch.can_allocate(small_order)

    def test_cannot_allocate_available_greater_the_required(self):
        """Нельзя добавить в заказ больше что есть в партии"""
        small_batch, large_order = make_batch_and_order_line("СТОЛ", 2, 20)
        assert small_batch.can_allocate(large_order) is False

    def test_can_allocate_if_available_equals_required(self):
        """Равно можно добавить в партию"""
        batch, order = make_batch_and_order_line("СТОЛ", 2, 2)
        assert batch.can_allocate(order)

    def test_cannot_allocate_if_sku_not_match(self):
        """Нельзя добавить с разным SKU"""
        batch = BatchDomain("batch-001", "ЛАМПА", 10)
        order_line = OrderLineDomain("order_line-001", "СТОЛ", 10)

        assert batch.can_allocate(order_line) is False


class TestAllocate:
    def test_allocate_batch_reduce_available_qty(self):
        """Проверка уменьшения партии на кол-во товаров в заказе"""
        batch, order_line = make_batch_and_order_line("СТУЛ", 20, 2)

        batch.allocate(order_line)
        assert batch.available_quantity == 18

    def test_allocate_is_idempotent(self):
        """При размещении одного и того же товара в той же партии, кол-во не должно изменится"""
        batch, order_line = make_batch_and_order_line("СТУЛ", 20, 2)
        batch.allocate(order_line)
        batch.allocate(order_line)
        assert batch.available_quantity == 18


class TestDeallocate:
    def test_can_only_deallocate_allocated_lines(self):
        """Если нет товара то и отменять не надо"""
        batch, not_allocated_order_line = make_batch_and_order_line("СТУЛ", 20, 2)
        batch.deallocate(not_allocated_order_line)

        assert batch.available_quantity == 20

    def test_deallocate(self):
        """Проверка отмены заказа"""
        batch, order_line = make_batch_and_order_line("СТУЛ", 20, 2)

        batch.allocate(order_line)
        assert batch.available_quantity == 18

        batch.deallocate(order_line)
        assert batch.available_quantity == 20
