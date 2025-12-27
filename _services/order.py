import requests

from _services.base_service import BaseService
from schemas.order_schema import OrderSchema, OrderResponse


class OrderService(BaseService):
    def get_order(self, order_id: str):
        url = f'{self._base_url}accounts/{self._account_id}/orders/{order_id}'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return OrderResponse.from_dict(response.json())
        return None

    def get_orders(self):
        url = f'{self._base_url}accounts/{self._account_id}/orders'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return [OrderSchema.from_dict(o['order']) for o in response.json()['orders']]
        return None

    def place_order(self, order: OrderSchema) -> None:
        url = f'{self._base_url}accounts/{self._account_id}'
        response = requests.get(url, headers=self._headers(), params=order.to_dict())
        if response.status_code == 200:
            return OrderResponse.from_dict(response.json())
        return None

    def cancel_order(self, order_id: str) -> None:
        url = f'{self._base_url}accounts/{self._account_id}/orders/{order_id}'
        response = requests.delete(url, headers=self._headers())
        if response.status_code == 200:
            return OrderResponse.from_dict(response.json())
        return None