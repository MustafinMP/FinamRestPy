from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from finam_rest_py.models.converters import date_from_dict


@dataclass
class Asset:
    id: str
    ticker: str
    mic: str
    isin: str
    type: str
    name: str

    def symbol(self) -> str:
        return f'{self.ticker}@{self.mic}'

    @classmethod
    def from_dict(cls, asset_dict: dict) -> Asset:
        return Asset(
            id=asset_dict['id'],
            ticker=asset_dict['ticker'],
            mic=asset_dict['mic'],
            isin=asset_dict['isin'],
            type=asset_dict['type'],
            name=asset_dict['name'],
        )


@dataclass
class FullAsset(Asset):
    decimals: int
    min_step: int
    lot_size: float
    expiration_date: Optional[datetime, None]
    quote_currency: Optional[str | None]

    @classmethod
    def from_dict(cls, asset_dict: dict) -> FullAsset:
        return FullAsset(
            id=asset_dict['id'],
            ticker=asset_dict['ticker'],
            mic=asset_dict['mic'],
            isin=asset_dict['isin'],
            type=asset_dict['type'],
            name=asset_dict['name'],
            decimals=int(asset_dict['decimals']),
            min_step=int(asset_dict['min_step']),
            lot_size=int(float(asset_dict['lot_size']['value'])),
            expiration_date=date_from_dict(
                asset_dict['expiration_date']) if 'expiration_date' in asset_dict else None,
            quote_currency=asset_dict.get('quote_currency', None)
        )
