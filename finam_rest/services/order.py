import requests

from finam_rest.services.base_service import BaseService
from finam_rest.models import Order, FullOrder


class OrderService(BaseService):
    def get_order(self, order_id: str) -> FullOrder:
        url = f'{self._base_url}accounts/{self._account_id}/orders/{order_id}'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        return None

    def get_orders(self) -> list[FullOrder]:
        url = f'{self._base_url}accounts/{self._account_id}/orders'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return [FullOrder.from_dict(o) for o in response.json()['orders']]
        return None

    def place_order(self, order: Order) -> FullOrder:
        url = f'{self._base_url}accounts/{self._account_id}/orders'
        response = requests.post(url, headers=self._headers(), json=order.to_dict())
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        return None

    def cancel_order(self, order_id: str) -> FullOrder:
        url = f'{self._base_url}accounts/{self._account_id}/orders/{order_id}'
        response = requests.delete(url, headers=self._headers())
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        return None