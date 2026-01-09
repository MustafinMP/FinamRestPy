from datetime import datetime

import requests

from _services.base_service import BaseService
from schemas.market_schemas import BarsResponse, TimeFrame, QuoteSchema, LatestTradesResponse, OrderBookSchema


class MarketService(BaseService):
    def get_bars(
            self,
            symbol: str,
            timeframe: TimeFrame,
            end_time: datetime,
            start_time: datetime = None
    ) -> BarsResponse:
        url = f'{self._base_url}instruments/{symbol}/bars'
        params = {
            'symbol': symbol,
            'timeframe': timeframe.value,
            'interval.end_time': end_time.isoformat() + 'Z'
        }
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'

        response = requests.get(url, headers=self._headers(), params=params)
        if response.status_code == 200:
            return BarsResponse.from_dict(response.json())
        return None

    def get_last_quote(self, symbol: str) -> QuoteSchema:
        url = f'{self._base_url}instruments/{symbol}/quotes/latest'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return QuoteSchema.from_dict(response.json())
        return None

    def get_latest_trades(self, symbol: str) -> LatestTradesResponse:
        url = f'{self._base_url}instruments/{symbol}/trades/latest'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return LatestTradesResponse.from_dict(response.json())
        return None

    def get_order_book(self, symbol: str) -> OrderBookSchema:
        url = f'{self._base_url}instruments/{symbol}/orderbook'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return OrderBookSchema.from_dict(response.json())
        return None
