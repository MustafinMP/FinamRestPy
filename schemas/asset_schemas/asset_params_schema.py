from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from schemas.money_schema import MoneySchema


class LongableStatus(Enum):
    NOT_AVAILABLE = 0  # Не доступен
    AVAILABLE = 1  # Доступен
    ACCOUNT_NOT_APPROVED = 2  # Запрещено на уровне счета

    @classmethod
    def from_str(cls, string: str) -> LongableStatus:
        match string:
            case 'NOT_AVAILABLE':
                return cls.NOT_AVAILABLE
            case 'AVAILABLE':
                return cls.AVAILABLE
            case 'ACCOUNT_NOT_APPROVED':
                return cls.ACCOUNT_NOT_APPROVED
            case _:
                return cls.NOT_AVAILABLE


class ShortableStatus(Enum):
    NOT_AVAILABLE = 0  # Не доступен
    AVAILABLE = 1  # Доступен
    HTB = 2  # Признак того, что бумага Hard To Borrow(если есть)
    ACCOUNT_NOT_APPROVED = 3  # Запрещено на уровне счета
    AVAILABLE_STRATEGY = 4  # Разрешено в составе стратег

    @classmethod
    def from_str(cls, string: str) -> LongableStatus:
        match string:
            case 'NOT_AVAILABLE':
                return cls.NOT_AVAILABLE
            case 'AVAILABLE':
                return cls.AVAILABLE
            case 'HTB':
                return cls.HTB
            case 'ACCOUNT_NOT_APPROVED':
                return cls.ACCOUNT_NOT_APPROVED
            case 'AVAILABLE_STRATEGY':
                return cls.AVAILABLE_STRATEGY
            case _:
                return cls.NOT_AVAILABLE


class PriceType(Enum):
    UNKNOWN = 0  # Неизвестно
    POSITIVE = 1  # Положительная.Больше нуля
    NON_NEGATIVE = 2  # Неотрицательная. Больше или равна нулю
    ANY = 3  # Любая

    @classmethod
    def from_str(cls, string: str) -> PriceType:
        match string:
            case 'UNKNOWN':
                return cls.UNKNOWN
            case 'POSITIVE':
                return cls.POSITIVE
            case 'NON_NEGATIVE':
                return cls.NON_NEGATIVE
            case 'ANY':
                return cls.ANY
            case _:
                return cls.UNKNOWN


@dataclass
class AssetParamsSchema:
    symbol: str
    account_id: str
    is_tradable: bool
    longable_status: LongableStatus
    longable_halted_days: int
    shortable_status: str
    shortable_halted_days: int
    long_risk_rate: float
    long_collateral: MoneySchema
    short_risk_rate: float
    short_collateral: MoneySchema
    long_initial_margin: Optional[MoneySchema, None]
    short_initial_margin: Optional[MoneySchema, None]
    price_type: str

    @classmethod
    def from_dict(cls, params_dict: dict) -> AssetParamsSchema:
        return AssetParamsSchema(
            symbol=params_dict['symbol'],
            account_id=params_dict['account_id'],
            is_tradable=params_dict['is_tradable'],
            longable_status=LongableStatus.from_str(params_dict['longable']['value']),
            longable_halted_days=int(params_dict['longable']['halted_days']),
            shortable_status=ShortableStatus.from_str(params_dict['shortable']['value']),
            shortable_halted_days=int(params_dict['shortable']['halted_days']),
            long_risk_rate=float(params_dict['long_risk_rate']['value']),
            long_collateral=MoneySchema.from_dict(params_dict['long_collateral']),
            short_risk_rate=float(params_dict['short_risk_rate']['value']),
            short_collateral=MoneySchema.from_dict(params_dict['short_collateral']),
            long_initial_margin=MoneySchema.from_dict(
                params_dict['long_initial_margin']) if 'long_initial_margin' in params_dict.keys() else None,
            short_initial_margin=MoneySchema.from_dict(
                params_dict['short_initial_margin']) if 'short_initial_margin' in params_dict.keys() else None,
            price_type=PriceType.from_str(params_dict['price_type'])
        )
