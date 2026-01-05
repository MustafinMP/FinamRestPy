import json

import requests

from _services.account import AccountService
from _services.assets import AssetService
from _services.market import MarketService
from _services.metrics import MetricsService
from _services.order import OrderService


class Finam:
    _base_url = 'https://api.finam.ru/v1/'

    def __init__(self, user_token: str, account_id: str):
        super().__init__()
        self._account_id = account_id
        self._user_token = user_token
        response = requests.post(
            f'{self._base_url}sessions',
            data=json.dumps({'secret': self._user_token}),
            headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
        )
        self._jwt_token = response.json()['token']

        self.account = AccountService(self._jwt_token, self._account_id, self._base_url)
        self.instruments = AssetService(self._jwt_token, self._account_id, self._base_url)
        self.orders = OrderService(self._jwt_token, self._account_id, self._base_url)
        self.market = MarketService(self._jwt_token, self._account_id, self._base_url)
        self.metrics = MetricsService(self._jwt_token, self._account_id, self._base_url)

    def set_account(self, account_id: str) -> None:
        self._account_id = account_id
        self.account.set_account(account_id)
        self.instruments.set_account(account_id)
        self.orders.set_account(account_id)
        self.market.set_account(account_id)
        self.metrics.set_account(account_id)

    def _headers(self):
        return {"Authorization": f"{self._jwt_token}", 'Content-Type': 'application/json', 'Accept': 'application/json'}
