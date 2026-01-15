import json
import threading
import time
from typing import Optional

import aiohttp
import requests

from finam_rest_py.services.account import AccountService
from finam_rest_py.services.assets import AssetService
from finam_rest_py.services.async_metrics import MetricsService
from finam_rest_py.services.market import MarketService
from finam_rest_py.services.async_metrics import MetricsService
from finam_rest_py.services.order import OrderService


class Finam:
    _base_url = 'https://api.finam.ru/v1/'
    _jwt_token_dict = dict()
    _lock = threading.Lock()

    def __init__(self, user_token: str, account_id: str):
        super().__init__()
        self._account_id = account_id
        self._user_token = user_token

        self._session: Optional[aiohttp.ClientSession] = None

        self.account = AccountService(self)
        self.instruments = AssetService(self._base_url, self._account_id)
        self.orders = OrderService(self)
        self.market = MarketService(self)
        self.metrics = MetricsService(self)

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
            self.instruments._set_jwt_token(token)

    def _update_jwt_token_loop(self) -> None:
        period_in_seconds = 14 * 60 + 30

        while True:
            self._update_jwt_token()
            time.sleep(period_in_seconds)

    def _get_session(self) -> aiohttp.ClientSession:
        """Получение или создание сессии"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                base_url=self._base_url,
                headers=self._headers(),
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self._session

    def set_account(self, account_id: str) -> None:
        self._account_id = account_id
        self.instruments.set_account(account_id)

    def get_account(self) -> str:
        return self._account_id

    def _headers(self):
        return {"Authorization": f"{self._jwt_token_dict[self._user_token]}", 'Content-Type': 'application/json',
                'Accept': 'application/json'}

    def __del__(self):
        self._jwt_thread.join()
