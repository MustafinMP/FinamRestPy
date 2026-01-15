from datetime import datetime

import requests

from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.services.base_service import BaseService
from finam_rest_py.models import Account, AccountTrade, Transaction


class AccountService(BaseService):
    def get_account(self) -> Account:
        url = f'{self._base_url}accounts/{self._account_id}'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return Account.from_dict(response.json())
        raise ResponseFailureException

    def get_trades(self, end_time: datetime, start_time: datetime = None, limit: int = None) -> list[AccountTrade]:
        url = f'{self._base_url}accounts/{self._account_id}/trades'
        params = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = requests.get(url, params=params, headers=self._headers())
        if response.status_code == 200:
            return [AccountTrade.from_dict(t) for t in response.json()['trades']]
        raise ResponseFailureException

    def transactions(self, end_time: datetime, start_time: datetime = None, limit: int = None) -> list[Transaction]:
        url = f'{self._base_url}accounts/{self._account_id}/transactions'
        params = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = requests.get(url, params=params, headers=self._headers())
        if response.status_code == 200:
            return [Transaction.from_dict(t) for t in response.json()['transactions']]
        raise ResponseFailureException
