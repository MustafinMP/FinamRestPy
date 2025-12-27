from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class BarSchema:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    @classmethod
    def from_dict(cls, bar_dict: dict) -> BarSchema:
        return BarSchema(
            timestamp=datetime.strptime(bar_dict['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            open=float(bar_dict['open']['value']),
            high=float(bar_dict['high']['value']),
            low=float(bar_dict['low']['value']),
            close=float(bar_dict['close']['value']),
            volume=int(bar_dict['volume']['value']),
        )
