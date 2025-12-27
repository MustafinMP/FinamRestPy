from __future__ import annotations

from enum import Enum


class OrderStopCondition(Enum):
    STOP_CONDITION_UNSPECIFIED = 0  # Значение не указано
    STOP_CONDITION_LAST_UP = 1  # Цена срабатывания больше текущей цены
    STOP_CONDITION_LAST_DOWN = 2  # Цена срабатывания меньше текущей цены

    @classmethod
    def from_str(cls, string: str) -> OrderStopCondition:
        match string:
            case 'STOP_CONDITION_UNSPECIFIED':
                return cls.STOP_CONDITION_UNSPECIFIED
            case 'STOP_CONDITION_LAST_UP':
                return cls.STOP_CONDITION_LAST_UP
            case 'STOP_CONDITION_LAST_DOWN':
                return cls.STOP_CONDITION_LAST_DOWN
            case _:
                return cls.STOP_CONDITION_UNSPECIFIED
