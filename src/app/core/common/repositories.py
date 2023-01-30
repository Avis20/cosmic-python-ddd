from abc import ABC
from typing import Any, List


class BaseRepository(ABC):
    def add(self):
        raise NotImplementedError

    def get(self, reference: Any):
        raise NotImplementedError

    def list(self) -> List[Any]:
        raise NotImplementedError
