from datetime import datetime

from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.models import Account, AccountTrade, Transaction
from finam_rest_py.services.async_base_service import AsyncBaseService


class AccountService(AsyncBaseService):
    async def get_account(self) -> Account:
        async with self._session.get(f'accounts/{self._account_id}') as response:
            if response.status == 200:
                return Account.from_dict(await response.json())
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

        async with self._session.get(f'accounts/{self._account_id}/trades', params=params) as response:
            if response.status == 200:
                return [AccountTrade.from_dict(t) for t in (await response.json())['trades']]
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

        async with self._session.get(f'accounts/{self._account_id}/transactions', params=params) as response:
            if response.status == 200:
                return [Transaction.from_dict(t) for t in (await response.json())['transactions']]
            raise ResponseFailureException
