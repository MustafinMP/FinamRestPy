from __future__ import annotations

from dataclasses import dataclass

from schemas.money_schema import MoneySchema
from schemas.position_schema import PositionSchema


@dataclass
class AccountSchema:
    account_id: str
    type: str
    status: str
    equity: float
    unrealized_profit: float
    positions: list[PositionSchema]
    cash: list[MoneySchema]

    # так как пока нет необходимости, не описаны данные по марже

    @classmethod
    def from_dict(cls, response_dict: dict) -> AccountSchema:
        return AccountSchema(
            account_id=str(response_dict['account_id']),
            type=str(response_dict['type']),
            status=str(response_dict['status']),
            equity=float(response_dict['type']['value']),
            unrealized_profit=float(response_dict['unrealized_profit']['value']),
            positions=[PositionSchema.from_dict(p) for p in response_dict['positions']],
            cash=[MoneySchema.from_dict(c) for c in response_dict['cash']]
        )
