import requests

from _services.base_service import BaseService


class MarketService(BaseService):
    def get_bars(self, symbol: str) -> ...:
        url = f'{self._base_url}instruments/{symbol}/bars'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return response.json()
        return None

    def get_last_quotes(self, symbol: str) -> ...:
        url = f'{self._base_url}instruments/{symbol}/quotes/latest'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return response.json()
        return None

    def get_trades(self, symbol: str) -> ...:
        url = f'{self._base_url}instruments/{symbol}/trades/latest'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return response.json()
        return None

    def get_order_book(self, symbol: str) -> ...:
        url = f'{self._base_url}instruments/{symbol}/orderbook'
        response = requests.get(url, headers=self._headers(), params={'symbol': symbol})
        if response.status_code == 200:
            return response.json()
        return None
