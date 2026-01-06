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

    def __init__(self, user_token: str, account_id: str):
        super().__init__()
        self._account_id = account_id
        self._user_token = user_token
        self._jwt_token = None

        self._lock = threading.Lock()

        self.account = AccountService(self._jwt_token, self._account_id, self._base_url)
        self.instruments = AssetService(self._jwt_token, self._account_id, self._base_url)
        self.orders = OrderService(self._jwt_token, self._account_id, self._base_url)
        self.market = MarketService(self._jwt_token, self._account_id, self._base_url)
        self.metrics = MetricsService(self._jwt_token, self._account_id, self._base_url)

        self._jwt_thread = threading.Thread(
            target=self._update_jwt_token,
            daemon=True
        )
        self._jwt_thread.start()

    def _update_jwt_token(self) -> None:
        period_in_seconds = 14 * 60 + 30

        while True:
            with self._lock:
                response = requests.post(
                    f'{self._base_url}sessions',
                    data=json.dumps({'secret': self._user_token}),
                    headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
                )
                self._jwt_token = response.json()['token']
                print('updated')
                self.account._update_jwt(self._jwt_token)
                self.instruments._update_jwt(self._jwt_token)
                self.orders._update_jwt(self._jwt_token)
                self.market._update_jwt(self._jwt_token)
                self.metrics._update_jwt(self._jwt_token)

            time.sleep(period_in_seconds)

    def set_account(self, account_id: str) -> None:
        self._account_id = account_id
        self.account.set_account(account_id)
        self.instruments.set_account(account_id)
        self.orders.set_account(account_id)
        self.market.set_account(account_id)
        self.metrics.set_account(account_id)

    def _headers(self):
        return {"Authorization": f"{self._jwt_token}", 'Content-Type': 'application/json', 'Accept': 'application/json'}

    def __del__(self):
        self._jwt_thread.join()
