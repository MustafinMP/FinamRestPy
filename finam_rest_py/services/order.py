from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.services.base_service import AsyncBaseService
from finam_rest_py.models import Order, FullOrder


class OrderService(AsyncBaseService):
    async def get_order(self, order_id: str) -> FullOrder:
        response = await self._session.get(f'accounts/{self._account_id}/orders/{order_id}')
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        raise ResponseFailureException

    async def get_orders(self) -> list[FullOrder]:
        response = await self._session.get(f'accounts/{self._account_id}/orders')
        if response.status_code == 200:
            return [FullOrder.from_dict(o) for o in response.json()['orders']]
        raise ResponseFailureException

    async def place_order(self, order: Order) -> FullOrder:
        response = await self._session.post(f'accounts/{self._account_id}/orders', json=order.to_dict())
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        raise ResponseFailureException

    async def cancel_order(self, order_id: str) -> FullOrder:
        response = await self._session.delete(f'accounts/{self._account_id}/orders/{order_id}')
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        raise ResponseFailureException