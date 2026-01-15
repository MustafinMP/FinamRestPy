from datetime import datetime

import requests

from finam_rest.services.base_service import BaseService
from finam_rest.models import Exchange, ScheduleSession, Asset, FullAsset, Option, AssetParams
from finam_rest.models.converters import formatted_datetime


class AssetService(BaseService):
    def get_assets(self) -> list[Asset]:
        url = f'{self._base_url}assets'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return [Asset.from_dict(a) for a in response.json()['assets']]
        print(response, response.reason)
        return None

    def get_clock(self) -> datetime:
        url = f'{self._base_url}assets/clock'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return formatted_datetime(response.json()['timestamp'])
        return None

    def get_exchanges(self) -> list[Exchange]:
        url = f'{self._base_url}exchanges'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return [Exchange.from_dict(e) for e in response.json()['exchanges']]
        return None

    def get_asset(self, symbol: str) -> FullAsset:
        url = f'{self._base_url}assets/{symbol}'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol, 'account_id': self._account_id})
        if response.status_code == 200:
            return FullAsset.from_dict(response.json())
        return None

    def get_asset_params(self, symbol: str, account_id: str = None):
        url = f'{self._base_url}assets/{symbol}/params'
        params = {'symbol': symbol, 'account_id': account_id if account_id else self._account_id}
        response = requests.get(url, headers=self._headers(), params=params)
        if response.status_code == 200:
            return AssetParams.from_dict(response.json())
        return None

    def get_options_chain(self, underlying_symbol: str,
                          root: str = None, expiration_date: datetime = None) -> list[Option]:
        url = f'{self._base_url}assets/{underlying_symbol}/options'
        params = {'underlying_symbol': underlying_symbol}
        if root:
            params['root'] = root
        if expiration_date:
            params['expiration_date.year'] = expiration_date.year
            params['expiration_date.month'] = expiration_date.month
            params['expiration_date.day'] = expiration_date.day
        response = requests.get(url, headers=self._headers(), params=params)
        if response.status_code == 200:
            return [Option.from_dict(op) for op in response.json()['options']]
        return None

    def get_schedule(self, symbol: str) -> list[ScheduleSession]:
        url = f'{self._base_url}assets/{symbol}/schedule'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return [ScheduleSession.from_dict(s) for s in response.json()['sessions']]
        return None
