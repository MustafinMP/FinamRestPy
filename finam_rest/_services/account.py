from datetime import datetime

import requests

from finam_rest._services.base_service import BaseService
from finam_rest.schemas.account_schemas import AccountSchema, AccountTradeSchema, TransactionSchema


class AccountService(BaseService):
    def get_account(self) -> AccountSchema:
        url = f'{self._base_url}accounts/{self._account_id}'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return AccountSchema.from_dict(response.json())
        return None

    def get_trades(self, end_time: datetime, start_time: datetime = None, limit: int = None) -> list[AccountTradeSchema]:
        url = f'{self._base_url}accounts/{self._account_id}/trades'
        params = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = requests.get(url, params=params, headers=self._headers())
        if response.status_code == 200:
            return [AccountTradeSchema.from_dict(t) for t in response.json()['trades']]
        return None

    def transactions(self, end_time: datetime, start_time: datetime = None, limit: int = None) -> list[TransactionSchema]:
        url = f'{self._base_url}accounts/{self._account_id}/transactions'
        params = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = requests.get(url, params=params, headers=self._headers())
        if response.status_code == 200:
            return [TransactionSchema.from_dict(t) for t in response.json()['transactions']]
        return None
