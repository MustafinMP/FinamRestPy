import requests

from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.services.async_base_service import AsyncBaseService
from finam_rest_py.services.base_service import BaseService
from finam_rest_py.models import Order, FullOrder


class OrderService(AsyncBaseService):
    async def get_order(self, order_id: str) -> FullOrder:
        async with self._session.get(f'accounts/{self._account_id}/orders/{order_id}') as response:
            if response.status == 200:
                return FullOrder.from_dict(await response.json())
            raise ResponseFailureException

    async def get_orders(self) -> list[FullOrder]:
        async with self._session.get(f'accounts/{self._account_id}/orders') as response:
            if response.status == 200:
                return [FullOrder.from_dict(o) for o in (await response.json())['orders']]
            raise ResponseFailureException

    async def place_order(self, order: Order) -> FullOrder:
        async with self._session.post(f'accounts/{self._account_id}/orders', json=order.to_dict()) as response:
            if response.status == 200:
                return FullOrder.from_dict(await response.json())
            raise ResponseFailureException

    async def cancel_order(self, order_id: str) -> FullOrder:
        async with self._session.delete(f'accounts/{self._account_id}/orders/{order_id}') as response:
            if response.status == 200:
                return FullOrder.from_dict(await response.json())
            raise ResponseFailureException