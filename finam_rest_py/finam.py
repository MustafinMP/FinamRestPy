import asyncio
import json
import threading
from typing import Optional

import httpx

from finam_rest_py.services.account import AccountService
from finam_rest_py.services.assets import AssetService
from finam_rest_py.services.market import MarketService
from finam_rest_py.services.metrics import MetricsService
from finam_rest_py.services.order import OrderService


class Finam:
    _base_url = 'https://api.finam.ru/v1/'
    _jwt_token_dict = dict()
    _lock = threading.Lock()

    def __init__(self, user_token: str, account_id: str):
        self.account = AccountService(self)
        self.instruments = AssetService(self)
        self.orders = OrderService(self)
        self.market = MarketService(self)
        self.metrics = MetricsService(self)

        self._account_id = account_id
        self._user_token = user_token

        self._session: Optional[httpx.AsyncClient] = None

        asyncio.run(self._refresh_jwt_token())
        self._refresh_token_thread = threading.Thread(
            target=asyncio.run,
            args=(self._refresh_jwt_token_loop(),),
            daemon=True
        )
        self._refresh_token_thread.start()

    async def _refresh_jwt_token(self) -> None:
        with Finam._lock:
            async with httpx.AsyncClient(
                    base_url=self._base_url,
                    headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                    timeout=30
            ) as session:
                response = await session.post(f'sessions', data=json.dumps({'secret': self._user_token}))
                self._jwt_token_dict[self._user_token] = response.json()['token']

    async def _refresh_jwt_token_loop(self) -> None:
        period_in_seconds = 14 * 60 + 30

        while True:
            await self._refresh_jwt_token()
            await asyncio.sleep(period_in_seconds)

    def _get_session(self) -> httpx.AsyncClient:
        """Получение или создание сессии"""
        if self._session is None or self._session.is_closed:
            self._session = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=30,
                headers=self._headers(),
                http2=True,
            )
        return self._session

    def _headers(self):
        return {"Authorization": f"{self._jwt_token_dict[self._user_token]}",
                'Content-Type': 'application/json',
                'Accept': 'application/json'}

    def set_account(self, account_id: str) -> None:
        self._account_id = account_id

    def get_account(self) -> str:
        return self._account_id

    def __del__(self):
        self._refresh_token_thread.join()
        asyncio.run(self._session.aclose())
