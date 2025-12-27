from __future__ import annotations

from dataclasses import dataclass

from schemas.market_schemas.bar import BarSchema


@dataclass
class BarsResponse:
    symbol: str
    bars: list[BarSchema]

    @classmethod
    def from_dict(cls, response_dict: dict) -> BarsResponse:
        return BarsResponse(
            symbol=response_dict['symbol'],
            bars=[BarSchema.from_dict(b) for b in response_dict['bars']]
        )