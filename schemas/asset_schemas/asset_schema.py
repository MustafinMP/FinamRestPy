from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from schemas.converters import datetime_from_dict


@dataclass
class AssetSchema:
    id: str
    ticker: str
    mic: str
    isin: str
    type: str
    name: str

    def symbol(self) -> str:
        return f'{self.ticker}@{self.mic}'

    @classmethod
    def from_dict(cls, asset_dict: dict) -> AssetSchema:
        return AssetSchema(
            id=asset_dict['id'],
            ticker=asset_dict['ticker'],
            mic=asset_dict['mic'],
            isin=asset_dict['isin'],
            type=asset_dict['type'],
            name=asset_dict['name'],
        )


@dataclass
class FullAssetSchema(AssetSchema):
    decimals: int
    min_step: int
    lot_size: float
    expiration_date: Optional[datetime, None]
    quote_currency: Optional[str | None]

    @classmethod
    def from_dict(cls, asset_dict: dict) -> FullAssetSchema:
        return FullAssetSchema(
            id=asset_dict['id'],
            ticker=asset_dict['ticker'],
            mic=asset_dict['mic'],
            isin=asset_dict['isin'],
            type=asset_dict['type'],
            name=asset_dict['name'],
            decimals=int(asset_dict['decimals']),
            min_step=int(asset_dict['min_step']),
            lot_size=int(asset_dict['lot_size']['value']),
            expiration_date=datetime_from_dict(asset_dict['expiration_date']),
            quote_currency=asset_dict.get('quote_currency', None)
        )
