from datetime import datetime

import requests

from _services.base_service import BaseService
from schemas.asset_schemas import ExchangeSchema, SessionSchema


class AssetService(BaseService):
    def get_assets(self):
        ...

    def get_clock(self) -> datetime:
        url = f'{self._base_url}assets/clock'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return datetime.strptime(response.json()['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        return None

    def get_exchanges(self) -> list[ExchangeSchema]:
        url = f'{self._base_url}exchanges'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return [ExchangeSchema.from_dict(e) for e in response.json()['exchanges']]
        return None

    def get_asset(self):
        ...

    def get_asset_params(self):
        ...

    def get_options_chain(self):
        ...

    def get_schedule(self, symbol: str) -> list[SessionSchema]:
        url = f'{self._base_url}/assets/{symbol}/schedule'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return [SessionSchema.from_dict(s) for s in response.json()['sessions']]
        return None

