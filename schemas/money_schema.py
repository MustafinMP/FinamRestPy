from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MoneySchema:
    currency_code: str
    units: int
    nanos: int

    @classmethod
    def from_dict(cls, response_dict: dict) -> MoneySchema:
        return MoneySchema(
            currency_code=str(response_dict['currency_code']),
            units=int(response_dict['units']),
            nanos=int(response_dict['nanos']) // (10 ** 7)
        )
