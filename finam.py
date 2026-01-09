import json
import threading
import time

import requests

from _services.account import AccountService
from _services.assets import AssetService
from _services.market import MarketService
from _services.metrics import MetricsService
from _services.order import OrderService


class Finam:
    _base_url = 'https://api.finam.ru/v1/'
    _jwt_token_dict = dict()
    _lock = threading.Lock()

    def __init__(self, user_token: str, account_id: str):
        super().__init__()
        self._account_id = account_id
        self._user_token = user_token

        self.account = AccountService(self._base_url, self._account_id)
        self.instruments = AssetService(self._base_url, self._account_id)
        self.orders = OrderService(self._base_url, self._account_id)
        self.market = MarketService(self._base_url, self._account_id)
        self.metrics = MetricsService(self._base_url, self._account_id)

        self._update_jwt_token()
        self._jwt_thread = threading.Thread(
            target=self._update_jwt_token_loop,
            daemon=True
        )
        self._jwt_thread.start()

    def _set_jwt_token(self, token: str) -> None:
        self._jwt_token_dict[self._user_token] = token

    def _update_jwt_token(self) -> None:
        with Finam._lock:
            response = requests.post(
                f'{self._base_url}sessions',
                data=json.dumps({'secret': self._user_token}),
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
            )
            token = response.json()['token']
            self._set_jwt_token(token)
            self.account._set_jwt_token(token)
            self.instruments._set_jwt_token(token)
            self.orders._set_jwt_token(token)
            self.market._set_jwt_token(token)
            self.metrics._set_jwt_token(token)

    def _update_jwt_token_loop(self) -> None:
        period_in_seconds = 14 * 60 + 30

        while True:
            self._update_jwt_token()
            time.sleep(period_in_seconds)

    def set_account(self, account_id: str) -> None:
        self._account_id = account_id
        self.account.set_account(account_id)
        self.instruments.set_account(account_id)
        self.orders.set_account(account_id)
        self.market.set_account(account_id)
        self.metrics.set_account(account_id)

    def _headers(self):
        return {"Authorization": f"{self._jwt_token_dict[self._user_token]}", 'Content-Type': 'application/json',
                'Accept': 'application/json'}

    def __del__(self):
        self._jwt_thread.join()
