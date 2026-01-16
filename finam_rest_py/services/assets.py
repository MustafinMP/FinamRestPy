from datetime import datetime

from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.models import Exchange, ScheduleSession, Asset, FullAsset, Option, AssetParams
from finam_rest_py.models.converters import formatted_datetime
from finam_rest_py.services.base_service import AsyncBaseService


class AssetService(AsyncBaseService):
    async def get_assets(self) -> list[Asset]:
        response = await self._session.get('assets')
        if response.status_code == 200:
            return [Asset.from_dict(a) for a in response.json()['assets']]
        raise ResponseFailureException

    async def get_clock(self) -> datetime:
        response = await self._session.get('assets/clock')
        if response.status_code == 200:
            return formatted_datetime(response.json()['timestamp'])
        raise ResponseFailureException

    async def get_exchanges(self) -> list[Exchange]:
        response = await self._session.get('exchanges')
        if response.status_code == 200:
            return [Exchange.from_dict(e) for e in response.json()['exchanges']]
        raise ResponseFailureException

    async def get_asset(self, symbol: str) -> FullAsset:
        response = await self._session.get(f'assets/{symbol}',
                                     params={'symbol': symbol, 'account_id': self._account_id})
        if response.status_code == 200:
            return FullAsset.from_dict(response.json())
        raise ResponseFailureException

    async def get_asset_params(self, symbol: str, account_id: str = None):
        params = {'symbol': symbol, 'account_id': account_id if account_id else self._account_id}
        response = await self._session.get(f'assets/{symbol}/params', params=params)
        if response.status_code == 200:
            return AssetParams.from_dict(response.json())
        raise ResponseFailureException

    async def get_options_chain(self,
                                underlying_symbol: str,
                                root: str = None,
                                expiration_date: datetime = None) -> list[Option]:
        params = {'underlying_symbol': underlying_symbol}
        if root:
            params['root'] = root
        if expiration_date:
            params['expiration_date.year'] = expiration_date.year
            params['expiration_date.month'] = expiration_date.month
            params['expiration_date.day'] = expiration_date.day
        response = await self._session.get(f'assets/{underlying_symbol}/options', params=params)
        if response.status_code == 200:
            return [Option.from_dict(op) for op in response.json()['options']]
        raise ResponseFailureException

    async def get_schedule(self, symbol: str) -> list[ScheduleSession]:
        response = await self._session.get(f'assets/{symbol}/schedule', params={'symbol': symbol})
        if response.status_code == 200:
            return [ScheduleSession.from_dict(s) for s in response.json()['sessions']]
        raise ResponseFailureException
