from sqlalchemy.orm import Session
from sqlalchemy.sql import select, text

from domain import OrderLine


def test_insert_and_check_order_lines(session: Session):
    session.execute(
        text(
            'INSERT INTO order_lines ("order_id", "sku", qty) VALUES'
            '("order-1", "СТУЛ", 12),'
            '("order-1", "СТОЛ", 10),'
            '("order-1", "ХЛЕБ", 1);'
        )
    )

    expected = [
        (OrderLine("order-1", "СТУЛ", 12),),
        (OrderLine("order-1", "СТОЛ", 10),),
        (OrderLine("order-1", "ХЛЕБ", 1),),
    ]
    assert session.execute(select(OrderLine)).fetchall() == expected


def test_add_order_lines_and_select(session: Session):
    row = ("order-1", "СТОЛ", 3)
    order_line = OrderLine(*row)
    session.add(order_line)
    session.commit()

    rows = list(session.execute(text("SELECT order_id, sku, qty FROM order_lines")))
    assert rows == [row]
