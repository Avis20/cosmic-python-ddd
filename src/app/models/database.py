import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

from app.settings import get_settings

settings = get_settings()

engine = sa.create_engine(
    settings.get_postgres_uri,
    echo=False,
)
metadata = sa.MetaData()
BaseModel = declarative_base(metadata=metadata)
