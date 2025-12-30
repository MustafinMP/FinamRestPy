from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from schemas.trade_side import TradeSide


@dataclass
class TradeSchema:
    symbol: str
    trade_id: str
    mpid: str
    timestamp: datetime
    price: float
    size: float
    side: TradeSide

    @classmethod
    def from_dict(cls, trade_dict: dict) -> TradeSchema:
        return TradeSchema(
            symbol=trade_dict['symbol'],
            trade_id=trade_dict['trade_id'],
            mpid=trade_dict['mpid'],
            timestamp=datetime.strptime(trade_dict['timestamp'], "%Y-%m-%dT%H:%M:%SZ"),
            price=float(trade_dict['price']['value']),
            size=float(trade_dict['size']['value']),
            side=TradeSide.from_str(trade_dict['side'])
        )