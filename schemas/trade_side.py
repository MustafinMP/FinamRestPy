from __future__ import annotations

from enum import Enum


class TradeSide(Enum):
    LONG = 'SIDE_BUY'
    SHORT = 'SIDE_SELL'
    BUY = 'SIDE_BUY'
    SELL = 'SIDE_SELL'

    @classmethod
    def from_str(cls, string: str) -> TradeSide:
        if string == 'SIDE_BUY':
            return cls.BUY
        if string == 'SIDE_SELL':
            return cls.SELL
        return None
