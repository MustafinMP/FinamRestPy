from datetime import datetime

import requests

from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.models import Bar, Trade, TimeFrame, Quote, OrderBook
from finam_rest_py.services.base_service import BaseService


class MarketService(BaseService):
    def get_bars(self, symbol: str, timeframe: TimeFrame, start_time: datetime, end_time: datetime) -> list[Bar]:
        url = f'{self._base_url}instruments/{symbol}/bars'
        if end_time - timeframe.max_deep() > start_time:
            start_time = end_time - timeframe.max_deep()
        params = {
            'symbol': symbol,
            'timeframe': timeframe.value,
            'interval.start_time': start_time.isoformat() + 'Z',
            'interval.end_time': end_time.isoformat() + 'Z'
        }

        response = requests.get(url, headers=self._headers(), params=params)
        if response.status_code == 200:
            return [Bar.from_dict(bar) for bar in response.json()['bars']]
        raise ResponseFailureException

    def get_last_quote(self, symbol: str) -> Quote:
        url = f'{self._base_url}instruments/{symbol}/quotes/latest'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return Quote.from_dict(response.json())
        raise ResponseFailureException

    def get_latest_trades(self, symbol: str) -> list[Trade]:
        url = f'{self._base_url}instruments/{symbol}/trades/latest'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return [Trade.from_dict(t) for t in response.json()['trades']]
        raise ResponseFailureException

    def get_order_book(self, symbol: str) -> OrderBook:
        url = f'{self._base_url}instruments/{symbol}/orderbook'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return OrderBook.from_dict(response.json())
        raise ResponseFailureException
