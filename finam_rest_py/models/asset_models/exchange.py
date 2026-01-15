from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Exchange:
    mic: str
    name: str

    @classmethod
    def from_dict(cls, exchange_dict: dict) -> Exchange:
        return Exchange(
            mic=exchange_dict['mic'],
            name=exchange_dict['name']
        )
