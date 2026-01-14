from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from finam_rest.schemas.converters import formatted_datetime


class Action(Enum):
    ACTION_UNSPECIFIED = 0  # Действие не указано
    ACTION_REMOVE = 1  # Удалить
    ACTION_ADD = 2  # Добавить
    ACTION_UPDATE = 3  # Обновить

    @classmethod
    def from_str(cls, string: str) -> Action:
        match string:
            case 'ACTION_UNSPECIFIED': return cls.ACTION_UNSPECIFIED
            case 'ACTION_REMOVE': return cls.ACTION_REMOVE
            case 'ACTION_ADD': return cls.ACTION_ADD
            case 'ACTION_UPDATE': return cls.ACTION_UPDATE
            case _: return cls.ACTION_UNSPECIFIED


@dataclass
class RowSchema:
    price: float
    sell_size: float
    buy_size: float
    action: Action
    mpid: str
    timestamp: datetime

    @classmethod
    def from_dict(cls, row_dict: dict) -> RowSchema:
        return RowSchema(
            price=float(row_dict['price']['value']),
            sell_size=float(row_dict['sell_size']['value']) if 'sell_size' in row_dict else 0,
            buy_size=float(row_dict['buy_size']['value']) if 'buy_size' in row_dict else 0,
            action=Action.from_str(row_dict['action']),
            mpid=row_dict['mpid'],
            timestamp=formatted_datetime(row_dict['timestamp'])
        )


@dataclass
class OrderBookSchema:
    symbol: str
    orderbook: list[RowSchema]

    @classmethod
    def from_dict(cls, order_book_dict: dict) -> OrderBookSchema:
        return OrderBookSchema(
            symbol=order_book_dict['symbol'],
            orderbook=[RowSchema.from_dict(r) for r in order_book_dict['orderbook']['rows']]
        )