from __future__ import annotations

from dataclasses import dataclass

from finam_rest_py.models.money import MoneyModel
from finam_rest_py.models.account_models.position import Position


@dataclass
class Account:
    account_id: str
    type: str
    status: str
    equity: float
    unrealized_profit: float
    positions: list[Position]
    cash: list[MoneyModel]

    # так как пока нет необходимости, не описаны данные по марже

    @classmethod
    def from_dict(cls, response_dict: dict) -> Account:
        return Account(
            account_id=str(response_dict['account_id']),
            type=str(response_dict['type']),
            status=str(response_dict['status']),
            equity=float(response_dict['equity']['value']),
            unrealized_profit=float(response_dict['unrealized_profit']['value']),
            positions=[Position.from_dict(p) for p in response_dict['positions']],
            cash=[MoneyModel.from_dict(c) for c in response_dict['cash']]
        )
