from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Order, FullOrder
from finam_rest_py.services.base_service import AsyncBaseService


class OrderService(AsyncBaseService):
    async def get_order(self, order_id: str) -> FullOrder:
        response = await self._session.get(f'accounts/{self._account_id}/orders/{order_id}')
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_orders(self) -> list[FullOrder]:
        response = await self._session.get(f'accounts/{self._account_id}/orders')
        if response.status_code == 200:
            return [FullOrder.from_dict(o) for o in response.json()['orders']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def place_order(self, order: Order) -> FullOrder:
        response = await self._session.post(f'accounts/{self._account_id}/orders', json=order.to_dict())
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def cancel_order(self, order_id: str) -> FullOrder:
        response = await self._session.delete(f'accounts/{self._account_id}/orders/{order_id}')
        if response.status_code == 200:
            return FullOrder.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)
