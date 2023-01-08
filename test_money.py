import pytest
from dataclasses import dataclass


@dataclass(frozen=True)
class Name:
    first_name: str
    last_name: str


@dataclass(frozen=True)
class Money:
    currency: str
    value: int

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Money) and self.currency == other.currency:
            return self.value == other.value
        return False

    def __add__(self, other: object) -> "Money":
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError
            return Money(self.currency, value=self.value + other.value)
        return NotImplemented

    def __sub__(self, other: object) -> "Money":
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise ValueError
            return Money(self.currency, value=self.value - other.value)
        return NotImplemented


class TestMoney:

    fiver = Money("rub", 5)
    tenner = Money("rub", 10)

    def test_equals(self):
        assert Money("rub", 10) == Money("rub", 10)

    def test_not_equals_currency(self):
        assert Money("rub", 10) != Money("usd", 10)

    def test_can_add_values_with_same_currency(self):
        assert self.fiver + self.fiver == self.tenner

    def test_can_subtract_money(self):
        assert self.tenner - self.fiver == self.fiver

    def test_add_different_currency(self):
        with pytest.raises(ValueError):
            Money("rub", 10) + Money("usd", 10)
