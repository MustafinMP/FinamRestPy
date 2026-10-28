from datetime import date

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models.corporation.bond_events import BondCouponEvent, BondAmortizationEvent, BondOfferEvent, \
    BondEvent
from finam_rest_py.models.corporation.dividend import Dividend
from finam_rest_py.models.corporation.split import Split
from finam_rest_py.services.base_service import AsyncBaseService


class CorporationService(AsyncBaseService):
    async def _get_bonds_events(
            self,
            symbol: str,
            date_from: date,
            date_to: date,
            desc: bool = False,
            limit: int = 1000,
            offset: int = 0,
            past: bool = False
    ) -> list[BondEvent]:
        url = 'bonds/' + ('past' if past else 'future')
        params = {
            'symbol': symbol,
            'date_from.year': date_from.year,
            'date_from.month': date_from.month,
            'date_from.day': date_from.day,
            'date_to.year': date_to.year,
            'date_to.month': date_to.month,
            'date_to.day': date_to.day,
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
                                      limit: int = 1000, offset: int = 0) -> list[BondEvent]:
        """Возвращает список запланированных событий по облигациям за период времени.

        Args:
            symbol: символ инструмента в формате ticker@mic.
            date_from: дата начала периода.
            date_to: дата конца периода.
            desc: сортировка по убыванию (по умолчанию False).
            limit: ограничение количества получаемых событий.
            offset: смещение получаемых событий.

        Returns:
            Список запланированных событий по облигациям.
        """
        return await self._get_bonds_events(symbol, date_from, date_to, desc, limit, offset)

    async def get_past_bonds_events(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                    limit: int = 1000, offset: int = 0) -> list[BondEvent]:
        """Возвращает список прошедших событий по облигациям за период времени.

        Args:
            symbol: символ инструмента в формате ticker@mic.
            date_from: дата начала периода.
            date_to: дата конца периода.
            desc: сортировка по убыванию (по умолчанию False).
            limit: ограничение количества получаемых событий.
            offset: смещение получаемых событий.

        Returns:
            Список прошедших событий по облигациям.
        """
        return await self._get_bonds_events(symbol, date_from, date_to, desc, limit, offset, past=True)

    async def get_future_coupons(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                       limit: int = 1000, offset: int = 0) -> list[BondCouponEvent]:
        """Возвращает список запланированных выплат купонов по облигациям за период времени.

        Args:
            symbol: символ инструмента в формате ticker@mic.
            date_from: дата начала периода.
            date_to: дата конца периода.
            desc: сортировка по убыванию (по умолчанию False).
            limit: ограничение количества получаемых событий.
            offset: смещение получаемых событий.

        Returns:
            Список запланированных выплат купонов по облигациям.
        """
        return [
            event
            for event in await self.get_future_bonds_events(symbol, date_from, date_to, desc, limit, offset)
            if isinstance(event, BondCouponEvent)
        ]

    async def get_past_coupons(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                     limit: int = 1000, offset: int = 0) -> list[BondCouponEvent]:
        """Возвращает список прошедших выплат купонов по облигациям за период времени.

        Args:
            symbol: символ инструмента в формате ticker@mic.
            date_from: дата начала периода.
            date_to: дата конца периода.
            desc: сортировка по убыванию (по умолчанию False).
            limit: ограничение количества получаемых событий.
            offset: смещение получаемых событий.

        Returns:
            Список прошедших выплат купонов по облигациям.
        """
        return [
            event
            for event in await self.get_past_bonds_events(symbol, date_from, date_to, desc, limit, offset)
            if isinstance(event, BondCouponEvent)
        ]

    async def get_future_dividends(self, symbol: str, desc: bool = False,
                                   limit: int = 1000, offset: int = 0) -> list[Dividend]:
        """Возвращает список запланированных выплат дивидендов.

        Args:
            symbol: символ инструмента в формате ticker@mic.
            desc: сортировка по убыванию (по умолчанию False).
            limit: ограничение количества получаемых событий.
            offset: смещение получаемых событий.

        Returns:
            Список запланированных выплат дивидендов.
        """
        url = '/future-dividends'
        params = {
            'symbol': symbol,
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
            return [Dividend.from_dict(d) for d in response.json()['dividends']]
        raise FinamResponseFailureException(response)

    async def get_past_dividends(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                                 limit: int = 1000, offset: int = 0) -> list[Dividend]:
        """Возвращает список прошедших выплат дивидендов.

        Args:
            symbol: символ инструмента в формате ticker@mic.
            date_from: дата начала периода.
            date_to: дата конца периода.
            desc: сортировка по убыванию (по умолчанию False).
            limit: ограничение количества получаемых событий.
            offset: смещение получаемых событий.

        Returns:
            Список прошедших выплат дивидендов.
        """
        url = '/past-dividends'
        params = {
            'symbol': symbol,
            'date_from.year': date_from.year,
            'date_from.month': date_from.month,
            'date_from.day': date_from.day,
            'date_to.year': date_to.year,
            'date_to.month': date_to.month,
            'date_to.day': date_to.day,
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
            return [Dividend.from_dict(d) for d in response.json()['dividends']]
        raise FinamResponseFailureException(response)

    async def get_future_splits(self, symbol: str, desc: bool = False,
                                limit: int = 1000, offset: int = 0) -> list[Split]:
        """Возвращает список запланированных сплитов по активу.

        Args:
            symbol: символ инструмента в формате ticker@mic.
            desc: сортировка по убыванию (по умолчанию False).
            limit: ограничение количества получаемых событий.
            offset: смещение получаемых событий.

        Returns:
            Список запланированных сплитов по активу.
        """
        url = '/splits/future'
        params = {
            'symbol': symbol,
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
            return [Split.from_dict(s) for s in response.json()['splits']]
        raise FinamResponseFailureException(response)

    async def get_past_splits(self, symbol: str, date_from: date, date_to: date, desc: bool = False,
                              limit: int = 1000, offset: int = 0) -> list[Split]:
        """Возвращает список прошедших сплитов по активу.

        Args:
            symbol: символ инструмента в формате ticker@mic.
            date_from: дата начала периода.
            date_to: дата конца периода.
            desc: сортировка по убыванию (по умолчанию False).
            limit: ограничение количества получаемых событий.
            offset: смещение получаемых событий.

        Returns:
            Список прошедших сплитов по активу.
        """
        url = '/splits/past'
        params = {
            'symbol': symbol,
            'date_from.year': date_from.year,
            'date_from.month': date_from.month,
            'date_from.day': date_from.day,
            'date_to.year': date_to.year,
            'date_to.month': date_to.month,
            'date_to.day': date_to.day,
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
            return [Split.from_dict(s) for s in response.json()['splits']]
        raise FinamResponseFailureException(response)
