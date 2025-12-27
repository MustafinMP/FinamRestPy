from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from schemas.trade_side import TradeSide


class OrderType(Enum):
    ORDER_TYPE_UNSPECIFIED = 0  # Значение не указано
    ORDER_TYPE_MARKET = 1  # Рыночная
    ORDER_TYPE_LIMIT = 2  # Лимитная
    ORDER_TYPE_STOP = 3  # Стоп заявка рыночная
    ORDER_TYPE_STOP_LIMIT = 4  # Стоп заявка лимитная
    ORDER_TYPE_MULTI_LEG = 5  # Мульти лег заявка

    @classmethod
    def from_str(cls, string: str):
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


class TypeInForce(Enum):
    TIME_IN_FORCE_UNSPECIFIED = 0  # Значение не указано
    TIME_IN_FORCE_DAY = 1  # До конца дня
    TIME_IN_FORCE_GOOD_TILL_CANCEL = 2  # Действителен до отмены
    TIME_IN_FORCE_GOOD_TILL_CROSSING = 3  # Действителен до пересечения
    TIME_IN_FORCE_EXT = 4  # Внебиржевая торговля
    TIME_IN_FORCE_ON_OPEN = 5  # На открытии биржи
    TIME_IN_FORCE_ON_CLOSE = 6  # На закрытии биржи
    TIME_IN_FORCE_IOC = 7  # Исполнить немедленно или отменить
    TIME_IN_FORCE_FOK = 8  # Исполнить полностью или отменить

    @classmethod
    def from_str(cls, string: str):
        match string:
            case 'TIME_IN_FORCE_UNSPECIFIED', _:
                return cls.TIME_IN_FORCE_UNSPECIFIED
            case 'TIME_IN_FORCE_DAY':
                return cls.TIME_IN_FORCE_DAY
            case 'TIME_IN_FORCE_GOOD_TILL_CANCEL':
                return cls.TIME_IN_FORCE_GOOD_TILL_CANCEL
            case 'TIME_IN_FORCE_GOOD_TILL_CROSSING':
                return cls.TIME_IN_FORCE_GOOD_TILL_CROSSING
            case 'TIME_IN_FORCE_EXT':
                return cls.TIME_IN_FORCE_EXT
            case 'TIME_IN_FORCE_ON_OPEN':
                return cls.TIME_IN_FORCE_ON_OPEN
            case 'TIME_IN_FORCE_ON_CLOSE':
                return cls.TIME_IN_FORCE_ON_CLOSE
            case 'TIME_IN_FORCE_IOC':
                return cls.TIME_IN_FORCE_IOC
            case 'TIME_IN_FORCE_FOK':
                return cls.TIME_IN_FORCE_FOK
            case _:
                return cls.TIME_IN_FORCE_UNSPECIFIED


class StopCondition(Enum):
    STOP_CONDITION_UNSPECIFIED = 0  # Значение не указано
    STOP_CONDITION_LAST_UP = 1  # Цена срабатывания больше текущей цены
    STOP_CONDITION_LAST_DOWN = 2  # Цена срабатывания меньше текущей цены

    @classmethod
    def from_str(cls, string: str):
        match string:
            case 'STOP_CONDITION_UNSPECIFIED':
                return cls.STOP_CONDITION_UNSPECIFIED
            case 'STOP_CONDITION_LAST_UP':
                return cls.STOP_CONDITION_LAST_UP
            case 'STOP_CONDITION_LAST_DOWN':
                return cls.STOP_CONDITION_LAST_DOWN
            case _:
                return cls.STOP_CONDITION_UNSPECIFIED


class ValidBefore(Enum):
    VALID_BEFORE_UNSPECIFIED = 0  # Значение не указано
    VALID_BEFORE_END_OF_DAY = 1  # До конца торгового дня
    VALID_BEFORE_GOOD_TILL_CANCEL = 2  # До отмены
    VALID_BEFORE_GOOD_TILL_DATE = 3  # До указанной даты - времени. Данный тип на текущий момент не поддерживается при выставлении заявки

    @classmethod
    def from_str(cls, string: str):
        match string:
            case 'VALID_BEFORE_UNSPECIFIED':
                return cls.VALID_BEFORE_UNSPECIFIED
            case 'VALID_BEFORE_END_OF_DAY':
                return cls.VALID_BEFORE_END_OF_DAY
            case 'VALID_BEFORE_GOOD_TILL_CANCEL':
                return cls.VALID_BEFORE_GOOD_TILL_CANCEL
            case 'VALID_BEFORE_GOOD_TILL_DATE':
                return cls.VALID_BEFORE_GOOD_TILL_DATE
            case _:
                return cls.VALID_BEFORE_UNSPECIFIED


@dataclass
class OrderSchema:
    account_id: str
    symbol: str
    quantity: float
    side: TradeSide
    type: OrderType
    time_in_force: TypeInForce
    limit_price: Optional[float | None]
    stop_price: Optional[float | None]
    stop_condition: Optional[StopCondition | None]
    client_order_id: Optional[str | None]
    valid_before: Optional[ValidBefore | None]
    comment: Optional[str | None]

    def to_dict(self) -> dict:
        order = {
            'account_id': self.account_id,
            'symbol': self.symbol,
            'quantity': {'value': str(self.quantity)},
            'side': 'SIDE_BUY' if self.side == TradeSide.LONG else 'SIDE_SELL',
            'type': self.type.value,
            'time_in_force': self.time_in_force.value
        }
        if self.limit_price:
            order['limit_price'] = {'value': str(self.limit_price)}
        if self.stop_price:
            order['stop_price'] = {'value': str(self.stop_price)}
        if self.stop_condition:
            order['stop_condition'] = self.stop_condition.value
        if self.client_order_id:
            order['client_order_id'] = self.client_order_id
        if self.valid_before:
            order['valid_before'] = self.valid_before.value
        if self.comment:
            order['comment'] = self.comment
        return order

    @classmethod
    def from_dict(cls, order_dict: dict) -> OrderSchema:
        return OrderSchema(
            account_id=order_dict['account_id'],
            symbol=order_dict['symbol'],
            quantity=float(order_dict['quantity']['value']),
            side=TradeSide.LONG if order_dict['side'] == 'SIDE_BUY' else TradeSide.SHORT,
            type=OrderType.from_str(order_dict['type']),
            time_in_force=TypeInForce.from_str(order_dict['time_in_force']),
            limit_price=float(order_dict['limit_price']['value']) if 'limit_price' in order_dict.keys() else None,
            stop_price=float(order_dict['stop_price']['value']) if 'stop_price' in order_dict.keys() else None,
            stop_condition=StopCondition.from_str(order_dict.get('stop_condition', None)),
            client_order_id=order_dict.get('client_order_id', None),
            valid_before=ValidBefore.from_str(order_dict.get('valid_before', None)),
            comment=order_dict.get('comment', None),
        )


@dataclass
class OrderResponse:
    order_id: str
    exec_id: str
    status: None
    order: OrderSchema
    transact_at: datetime

    @classmethod
    def from_dict(cls, order_dict: dict) -> OrderResponse:
        return OrderResponse(
            order_id=order_dict['order_id'],
            exec_id=order_dict['exec_id'],
            status=order_dict['order_status'],
            order=OrderSchema.from_dict(order_dict['order']),
            transact_at=datetime.strptime(order_dict['transact_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        )