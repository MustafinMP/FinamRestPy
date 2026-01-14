from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExchangeSchema:
    mic: str
    name: str

    @classmethod
    def from_dict(cls, exchange_dict: dict) -> ExchangeSchema:
        return ExchangeSchema(
            mic=exchange_dict['mic'],
            name=exchange_dict['name']
        )
