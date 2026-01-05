from datetime import datetime

import requests

from _services.base_service import BaseService
from schemas.asset_schemas import ExchangeSchema, SessionSchema, AssetSchema, FullAssetSchema, OptionSchema, \
    AssetParamsSchema
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

    def get_asset_params(self, symbol: str, account_id: str):
        url = f'{self._base_url}/assets/{symbol}/params'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol, 'account_id': account_id})
        if response.status_code == 200:
            return AssetParamsSchema.from_dict(response.json())
        return None

    def get_options_chain(self, underlying_symbol: str,
                          root: str = None, expiration_date: datetime = None) -> list[OptionSchema]:
        url = f'{self._base_url}/assets/{underlying_symbol}/options'
        params = {'underlying_symbol': underlying_symbol}
        if root:
            params['root'] = root
        if expiration_date:
            params['expiration_date.year'] = expiration_date.year
            params['expiration_date.month'] = expiration_date.month
            params['expiration_date.day'] = expiration_date.day
        response = requests.get(url, headers=self._headers(), params=params)
        if response.status_code == 200:
            return [OptionSchema.from_dict(op) for op in response.json()['options']]
        return None

    def get_schedule(self, symbol: str) -> list[SessionSchema]:
        url = f'{self._base_url}/assets/{symbol}/schedule'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return [SessionSchema.from_dict(s) for s in response.json()['sessions']]
        return None
