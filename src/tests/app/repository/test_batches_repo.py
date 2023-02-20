from sqlalchemy.orm import Session
from sqlalchemy.sql import text


from app.domain.batches import BatchDomain
from app.repository.batches import BatchRepository


def test_can_save_batch(session: Session):
    """Проверка что репозиторий может сохранить домен"""
    row = ("batch-1", "СТОЛ", 10, None)
    batch = BatchDomain(*row)

    repo = BatchRepository(session=session)
    repo.add(batch)
    session.commit()

    rows = list(session.execute(
        text("SELECT number, sku, qty, eta FROM batches WHERE number=:number"), dict(number=row[0])
    ))
    assert [row] == rows
