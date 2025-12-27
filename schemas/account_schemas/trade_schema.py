from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from schemas.trade_side import TradeSide


@dataclass
class AccountTradeSchema:
    trade_id: str
    symbol: str
    price: float
    size: float
    side: TradeSide
    timestamp: datetime
    order_id: str
    account_id: str

    @classmethod
    def from_dict(cls, response_dict: dict) -> AccountTradeSchema:
        return AccountTradeSchema(
            trade_id=response_dict['trade_id'],
            symbol=response_dict['symbol'],
            price=float(response_dict['price']['value']),
            size=float(response_dict['size']['value']),
            side=TradeSide.LONG if response_dict['side'] == 'SIDE_BUY' else TradeSide.SHORT,
            timestamp=datetime.strptime(response_dict['timestamp'], '%Y-%m-%dT%H:%M:%SZ'),
            order_id=response_dict['order_id'],
            account_id=response_dict['account_id']
        )

