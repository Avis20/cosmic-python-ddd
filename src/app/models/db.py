# ./src/app/models/db.py

from typing import Generator
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.settings import get_settings

settings = get_settings()

metadata = MetaData()
engine = create_engine(settings.get_postgres_uri, echo=True)

session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=True)


def get_session() -> Generator:
    with session_factory() as session:
        try:
            yield session
            session.commit()
        except SQLAlchemyError as sql_ex:
            session.rollback()
            raise sql_ex
        finally:
            session.close()
