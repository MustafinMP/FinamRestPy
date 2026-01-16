from datetime import datetime

from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.models import Account, AccountTrade, Transaction
from finam_rest_py.services.base_service import AsyncBaseService


class AccountService(AsyncBaseService):
    async def get_account(self) -> Account:
        response = await self._session.get(f'accounts/{self._account_id}')
        if response.status_code == 200:
            return Account.from_dict(response.json())
        raise ResponseFailureException

    async def get_trades(self,
                         end_time: datetime,
                         start_time: datetime = None,
                         limit: int = None) -> list[AccountTrade]:
        params = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = await self._session.get(f'accounts/{self._account_id}/trades', params=params)
        if response.status_code == 200:
            return [AccountTrade.from_dict(t) for t in response.json()['trades']]
        raise ResponseFailureException

    async def transactions(self,
                           end_time: datetime,
                           start_time: datetime = None,
                           limit: int = None) -> list[Transaction]:
        params = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = await self._session.get(f'accounts/{self._account_id}/transactions', params=params)
        if response.status_code == 200:
            return [Transaction.from_dict(t) for t in response.json()['transactions']]
        raise ResponseFailureException
