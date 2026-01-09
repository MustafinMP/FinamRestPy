from __future__ import annotations

from enum import Enum


class OrderType(Enum):
    ORDER_TYPE_UNSPECIFIED = 0  # Значение не указано
    ORDER_TYPE_MARKET = 1  # Рыночная
    ORDER_TYPE_LIMIT = 2  # Лимитная
    ORDER_TYPE_STOP = 3  # Стоп заявка рыночная
    ORDER_TYPE_STOP_LIMIT = 4  # Стоп заявка лимитная
    ORDER_TYPE_MULTI_LEG = 5  # Мульти лег заявка

    @classmethod
    def from_str(cls, string: str) -> OrderType:
        match string:
            case 'ORDER_TYPE_UNSPECIFIED':
                return cls.ORDER_TYPE_UNSPECIFIED
            case 'ORDER_TYPE_MARKET':
                return cls.ORDER_TYPE_MARKET
            case 'ORDER_TYPE_LIMIT':
                return cls.ORDER_TYPE_LIMIT
            case 'ORDER_TYPE_STOP':
                return cls.ORDER_TYPE_STOP
            case 'ORDER_TYPE_STOP_LIMIT':
                return cls.ORDER_TYPE_STOP_LIMIT
            case 'ORDER_TYPE_MULTI_LEG':
                return cls.ORDER_TYPE_MULTI_LEG
            case _:
                return cls.ORDER_TYPE_UNSPECIFIED
