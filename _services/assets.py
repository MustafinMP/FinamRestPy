from datetime import datetime

import requests

from _services.base_service import BaseService
from schemas.asset_schemas import ExchangeSchema, SessionSchema, AssetSchema, FullAssetSchema
from schemas.asset_schemas.option_schema import OptionSchema
from schemas.converters import formatted_datetime


class AssetService(BaseService):
    def get_assets(self) -> list[AssetSchema]:
        url = f'{self._base_url}assets'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return [AssetSchema.from_dict(a) for a in response.json()['assets']]
        return None

    def get_clock(self) -> datetime:
        url = f'{self._base_url}assets/clock'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return formatted_datetime(response.json()['timestamp'])
        return None

    def get_exchanges(self) -> list[ExchangeSchema]:
        url = f'{self._base_url}exchanges'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return [ExchangeSchema.from_dict(e) for e in response.json()['exchanges']]
        return None

    def get_asset(self, symbol: str) -> FullAssetSchema:
        url = f'{self._base_url}assets/{symbol}'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol, 'account_id': self._account_id})
        if response.status_code == 200:
            return FullAssetSchema.from_dict(response.json())
        return None

    def get_asset_params(self):
        ...

    def get_options_chain(self, underlying_symbol: str,
                          root: str = None, expiration_date: datetime = None) -> list[OptionSchema]:
        url = f'{self._base_url}/assets/{underlying_symbol}/options'
        response = requests.get(url, headers=self._headers(), params={'underlying_symbol': underlying_symbol})
        if response.status_code == 200:
            return [OptionSchema.from_dict(op) for op in response.json()['options']]
        return None

    def get_schedule(self, symbol: str) -> list[SessionSchema]:
        url = f'{self._base_url}/assets/{symbol}/schedule'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return [SessionSchema.from_dict(s) for s in response.json()['sessions']]
        return None
