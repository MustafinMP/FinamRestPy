from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PositionSchema:
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    daily_pnl: float
    unrealized_pnl: float

    @classmethod
    def from_dict(cls, response_dict: dict) -> PositionSchema:
        return PositionSchema(
            symbol=str(response_dict['symbol']),
            quantity=int(response_dict['quantity']['value']),
            average_price=float(response_dict['average_price']['value']),
            current_price=float(response_dict['current_price']['value']),
            daily_pnl=float(response_dict['daily_pnl']['value']),
            unrealized_pnl=float(response_dict['unrealized_pnl']['value'])
        )
