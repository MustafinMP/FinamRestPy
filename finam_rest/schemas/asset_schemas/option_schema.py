from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from finam_rest.schemas.converters import datetime_from_dict


class OptionType(Enum):
    TYPE_UNSPECIFIED = 0  # Неопределенное значение
    TYPE_CALL = 1  # Колл
    TYPE_PUT = 2  # Пут

    @classmethod
    def from_str(cls, string: str) -> OptionType:
        match string:
            case 'TYPE_UNSPECIFIED': return cls.TYPE_UNSPECIFIED
            case 'TYPE_CALL': return cls.TYPE_CALL
            case 'TYPE_PUT': return cls.TYPE_PUT
            case _: return cls.TYPE_UNSPECIFIED


@dataclass
class OptionSchema:
    symbol: str
    type: str
    contract_size: float
    trade_first_day: Optional[datetime, None]
    trade_last_day: datetime
    strike: float
    multiplier: Optional[float, None]
    expiration_first_day: datetime
    expiration_last_day: datetime

    @classmethod
    def from_dict(cls, option_dict: dict) -> OptionSchema:
        return OptionSchema(
            symbol=option_dict['symbol'],
            type=OptionType.from_str(option_dict['type']),
            contract_size=float(option_dict['contract_size']['value']),
            trade_first_day=datetime_from_dict(option_dict['trade_first_day']) if 'trade_first_day' in option_dict.keys()
            else None,
            trade_last_day=datetime_from_dict(option_dict['trade_last_day']),
            strike=float(option_dict['strike']['value']),
            multiplier=float(option_dict['multiplier']['value']) if 'multiplier' in option_dict.keys() else None,
            expiration_first_day=datetime_from_dict(option_dict['expiration_first_day']),
            expiration_last_day=datetime_from_dict(option_dict['expiration_last_day'])
        )
