from __future__ import annotations

from dataclasses import dataclass

from schemas.market_schemas.trade_schema import TradeSchema


@dataclass
class LatestTradesResponse:
    symbol: str
    trades: list[TradeSchema]

    @classmethod
    def from_dict(cls, response_dict: dict) -> LatestTradesResponse:
        return LatestTradesResponse(
            symbol=response_dict['symbol'],
            trades=[TradeSchema.from_dict(t) for t in response_dict['trades']]
        )