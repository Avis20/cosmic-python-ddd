# ./tests/test_api.py

from fastapi.testclient import TestClient
from datetime import date, timedelta

from uuid import uuid4
from app.main import app

client = TestClient(app)


def random_suffix():
    return uuid4().hex[:6]


def random_sku(name: str = ""):
    return f"sku-{name}-{random_suffix()}"


def random_batch(name: int):
    return f"batch-{name}-{random_suffix()}"


def random_order(name: int):
    return f"order-{name}-{random_suffix()}"


def test_read_main():
    """Базовый тест проверки 200 OK"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Cosmic"}


def test_allocation_persistend(add_stock):
    sku = random_sku()
    batch1, batch2 = random_batch(1), random_batch(2)
    order1, order2 = random_order(1), random_order(2)
    today = date.today()
    tomorrow = today + timedelta(days=1)

    add_stock([(batch1, sku, 10, today), (batch2, sku, 10, tomorrow)])
    order_line1 = {"order_id": order1, "sku": sku, "qty": 10}
    order_line2 = {"order_id": order2, "sku": sku, "qty": 10}

    # Первый заказ исчерпывает все товары партии 1
    response = client.post("/allocate", json=order_line1)
    assert response.status_code == 200
    assert response.json().get("batch_name") == batch1

    # Второй заказ должен пойти в партию 2
    response = client.post("/allocate", json=order_line2)
    assert response.status_code == 200
    assert response.json().get("batch_name") == batch2
