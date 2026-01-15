from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from finam_rest_py.models.converters import formatted_datetime
from finam_rest_py.models.trade_side import TradeSide


@dataclass
class Trade:
    trade_id: str
    mpid: str
    timestamp: datetime
    price: float
    size: float
    side: TradeSide

    @classmethod
    def from_dict(cls, trade_dict: dict) -> Trade:
        return Trade(
            trade_id=trade_dict['trade_id'],
            mpid=trade_dict['mpid'],
            timestamp=formatted_datetime(trade_dict['timestamp']),
            price=float(trade_dict['price']['value']),
            size=float(trade_dict['size']['value']),
            side=TradeSide.from_str(trade_dict['side'])
        )