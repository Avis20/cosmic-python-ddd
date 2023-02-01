
import pytest
from uuid import uuid4

from fastapi.testclient import TestClient
from datetime import date, timedelta
from app.main import app

client = TestClient(app)


def random_suffix():
    return uuid4().hex[:6]


def random_sku(name: str = ""):
    return f"sku-{name}-{random_suffix()}"


def random_batch(name: int = 1):
    return f"batch-{name}-{random_suffix()}"


def random_order(name: int = 1):
    return f"order-{name}-{random_suffix()}"


def test_read_main():
    """Базовый тест проверки 200 OK"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Cosmic"}

@pytest.mark.skip("Запускать с postgres БД")
def test_happy_allocate_batches(add_stock):
    sku, other_sku = random_sku(), random_sku("other")
    early_batch = random_batch(1)
    slow_batch = random_batch(2)
    other_batch = random_batch(3)

    today = date.today()
    tomorrow = today + timedelta(days=1)

    add_stock(
        [
            (early_batch, sku, 100, today),
            (slow_batch, sku, 100, tomorrow),
            (other_batch, other_sku, 100, today),
        ]
    )
    data = {"order_id": random_order(1), "sku": sku, "qty": 10}
    response = client.post("/allocate", json=data)
    assert response.status_code == 200
    assert response.json().get("batch_name") == early_batch


def test_unhappy_allocate():
    unknown_sku = random_sku()
    data = {"order_id": random_order(1), "sku": unknown_sku, "qty": 10}
    response = client.post("/allocate", json=data)
    assert response.status_code == 400
    assert response.json().get("detail", {}).get("error") == f"Недопустимый артикул {unknown_sku}"
