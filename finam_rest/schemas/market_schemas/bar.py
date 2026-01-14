from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from finam_rest.schemas.converters import formatted_datetime


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
            timestamp=formatted_datetime(bar_dict['timestamp']),
            open=float(bar_dict['open']['value']),
            high=float(bar_dict['high']['value']),
            low=float(bar_dict['low']['value']),
            close=float(bar_dict['close']['value']),
            volume=int(float(bar_dict['volume']['value'])),
        )
