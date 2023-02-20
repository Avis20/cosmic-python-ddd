# ./src/app/models/base.py

from dataclasses import asdict
from typing import List, Tuple, Any, Dict

from sqlalchemy import func, Column, TIMESTAMP


class BaseModelMixin(object):
    ts_create = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
    ts_modify = Column(
        TIMESTAMP(timezone=False),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    @classmethod
    def from_domain(cls, domain):
        clean_data = asdict(domain, dict_factory=cls.clear_domain)
        return cls(**clean_data)

    @classmethod
    def clear_domain(cls, data: List[Tuple[str, Any]]) -> Dict[str, Any]:
        result = {}
        for key, value in data:
            # Если в домене есть приватный атрибут, то пропускаем
            if key.startswith("_"):
                continue
            else:
                result[key] = value
        return result
