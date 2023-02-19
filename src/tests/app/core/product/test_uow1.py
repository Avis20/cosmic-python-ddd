# ./tests/app/core/batch/test_uow.py

import pytest
import threading
import traceback
import time
from tests.utils import random_order, random_batch, random_sku

from app.core.order_lines.domain import OrderLineDomain
from app.core.product.uow import ProductUnitOfWork


def try_to_allocate(session_factory, order_id, sku, exceptions: list):
    line = OrderLineDomain(order_id, sku, 10)
    uow = ProductUnitOfWork(session_factory)
    try:
        with uow:
            product = uow.repository.get(sku)
            assert product is not None
            product.allocate(line)
            # time.sleep(0.2)
            uow.commit()
    except Exception as e:
        print(traceback.format_exc())
        exceptions.append(e)


def run_in_thread(functions):
    for func in functions:
        thread = threading.Thread(target=func)
        thread.start()
        thread.join()

@pytest.mark.skip("Т.к. БД запущена в памяти, 2-й процесс не видит БД")
def test_try_allocate(session_factory, add_stock):

    session = session_factory()
    sku, batch = random_sku(), random_batch(1)
    add_stock(lines=[[batch, sku, 10, None]], version=0)

    order_id1, order_id2 = random_order(1), random_order(2)
    exceptions = []
    try_to_allocate_order1 = lambda: try_to_allocate(session_factory, order_id1, sku, exceptions)
    try_to_allocate_order2 = lambda: try_to_allocate(session_factory, order_id2, sku, exceptions)

    run_in_thread([try_to_allocate_order1, try_to_allocate_order2])

    uow = ProductUnitOfWork(session_factory)
    with uow:
        product = uow.repository.get(sku)
        assert product is not None
        assert product.version_number == 1

    [exceptions] = exceptions
    assert "Не найдено подходящей партии товара" == str(exceptions)

    orders = session.execute(
        "SELECT a.order_line_id FROM public.allocations AS a "
        "JOIN public.batches AS b ON b.id = a.batch_id "
        "JOIN public.order_lines AS ol ON ol.id = a.order_line_id "
        "WHERE ol.sku = :sku",
        dict(sku=sku)
    )
    assert orders.rowcount == 1

