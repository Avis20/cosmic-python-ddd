from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    currency: str
    value: int

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Money):
            return self.value == other.value
        return False
    
    def __add__(self, other):


test1 = Money("rub", 10)
print(test1 == 10)
