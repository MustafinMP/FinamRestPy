from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Dividend:
    date: date
    amount: float
    currency: str

    @classmethod
    def from_dict(cls, data: dict) -> Dividend:
        return Dividend(
            date=date(year=data['date']['year'], month=data['date']['month'], day=data['date']['day']),
            amount=float(data['amount']['value']),
            currency=data['currency']
        )
