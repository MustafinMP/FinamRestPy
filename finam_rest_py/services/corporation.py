from datetime import date

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models.corporation.bond_events import BondCouponEvent, BondAmortizationEvent, BondOfferEvent, \
    BondEvent
from finam_rest_py.services.base_service import AsyncBaseService


class CorporationService(AsyncBaseService):
    async def _get_bonds_events(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                limit: int | None = None, offset: int | None = None, past: bool = False) -> list[
        BondEvent]:
        """получает метрики об использовании API.

        Returns:
            None

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        url = 'bonds/' + 'past' if past else 'future'
        params = {
            'symbol': symbol,
            'date_from.year': date_from.year,
            'date_from.month': date_from.month,
            'date_from.day': date_from.day,
            'date_to.year': date_to.year,
            'date_to.month': date_to.month,
            'date_to.day': date_to.day,
            'date_to': date_to,
            'sort_direction': 'DESC' if desc else 'ASC',
        }
        if limit:
            params['limit'] = str(limit)
        if offset:
            params['offset'] = str(offset)

        response = await self._session.get(url, params=params)
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(url, params=params)
        if response.status_code == 200:
            event_types = {'COUPON': BondCouponEvent, 'AMORTIZATION': BondAmortizationEvent, 'OFFER': BondOfferEvent}
            return [event_types[event['type']].from_dict(event) for event in response.json()['events']]
        raise FinamResponseFailureException(response)

    async def get_future_bonds_events(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                      limit: int | None = None, offset: int | None = None) -> list[BondEvent]:
        return await self._get_bonds_events(symbol, date_from, date_to, desc, limit, offset)

    async def get_past_bonds_events(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                    limit: int | None = None, offset: int | None = None) -> list[BondEvent]:
        return await self._get_bonds_events(symbol, date_from, date_to, desc, limit, offset, past=True)

    async def get_future_bonds_coupons(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                       limit: int | None = None, offset: int | None = None) -> list[BondCouponEvent]:
        return [
            event
            for event in await self.get_future_bonds_events(symbol, date_from, date_to, desc, limit, offset)
            if isinstance(event, BondCouponEvent)
        ]

    async def get_past_bonds_coupons(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                     limit: int | None = None, offset: int | None = None) -> list[BondCouponEvent]:
        return [
            event
            for event in await self.get_past_bonds_events(symbol, date_from, date_to, desc, limit, offset)
            if isinstance(event, BondCouponEvent)
        ]
