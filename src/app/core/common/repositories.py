from abc import ABC
from typing import Any, List


class AbstractRepository(ABC):
    def add(self, reference: Any):
        raise NotImplementedError

    def get(self, reference: Any):
        raise NotImplementedError

    def list(self) -> List[Any]:
        raise NotImplementedError
