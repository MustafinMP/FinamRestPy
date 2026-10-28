from datetime import datetime

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Bar, AssetTrade, TimeFrame, Quote, OrderBook
from finam_rest_py.services.base_service import AsyncBaseService


class MarketService(AsyncBaseService):
    async def _get_bars_batch(self, symbol: str, params: dict) -> list[Bar]:
        response = await self._session.get(f'instruments/{symbol}/bars', params=params)
        if response.status_code == 401:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'instruments/{symbol}/bars', params=params)

        if response.status_code == 200:
            return [Bar.from_dict(bar) for bar in response.json()['bars']]
        else:
            raise FinamResponseFailureException(response)

    async def get_bars(self,
                       symbol: str,
                       timeframe: TimeFrame | str,
                       start_time: datetime,
                       end_time: datetime) -> list[Bar]:
        """Получает свечи по инструменту в нужном таймфрейме.
        Предупреждение: API имеет два важных ограничения:
        - Ограничение на диапазон дат у выгружаемых свечей, которое зависит от таймфрейма
         (узнать диапазон можно с помощью timeframe.max_date_range())
        - Ограничение на 200 запросов в минуту
        (узнать оставшийся лимит можно с помощью finam.metrics.get_usage_metrics())

        Попытка выгрузки свечей с мелким таймфреймом по нескольким активам на широком диапазоне дат
         может потенциально столкнуться с ограничениями.
         Учитывайте время на восстановление лимитов.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.
            timeframe (TimeFrame | str): таймфрейм свечей.
            start_time (datetime): начало запрашиваемого периода.
            end_time (datetime): конец запрашиваемого периода.

        Returns:
            list[Bar]: список свечей.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        if isinstance(timeframe, str):
            timeframe = TimeFrame.from_str(timeframe)
        full_date_range = end_time - start_time
        if full_date_range > timeframe.max_date_range() * 200:
            raise ValueError('Слишком широкий диапазон дат')
        bars = []
        start_batch_time = start_time
        end_batch_time = start_time + timeframe.max_date_range()
        while end_batch_time <= end_time:
            params = {
                'symbol': symbol,
                'timeframe': timeframe.value,
                'interval.start_time': start_batch_time.isoformat() + 'Z',
                'interval.end_time': min(end_batch_time, end_time).isoformat() + 'Z'
            }
            batch = await self._get_bars_batch(symbol, params)
            bars.extend(batch)
            start_batch_time = end_batch_time
            end_batch_time = start_batch_time + timeframe.max_date_range()

        return bars

    async def get_last_quote(self, symbol: str) -> Quote:
        """Получает последнюю котировку по инструменту.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.

        Returns:
            Quote: последняя котировка по инструменту.

        Raises:
            ValueError: если запрошен слишком большой диапазон.
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'instruments/{symbol}/quotes/latest', params={'symbol': symbol})
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'instruments/{symbol}/quotes/latest', params={'symbol': symbol})

        if response.status_code == 200:
            return Quote.from_dict(response.json()['quote'])
        raise FinamResponseFailureException(response)

    async def get_latest_trades(self, symbol: str) -> list[AssetTrade]:
        """Получает данные о последних сделках по инструменту.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.

        Returns:
            list[Trade]: список последних сделок.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'instruments/{symbol}/trades/latest', params={'symbol': symbol})
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'instruments/{symbol}/trades/latest', params={'symbol': symbol})

        if response.status_code == 200:
            return [AssetTrade.from_dict(t) for t in response.json()['trades']]
        raise FinamResponseFailureException(response)

    async def get_order_book(self, symbol: str) -> OrderBook:
        """Получает книгу заявок по инструменту.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.

        Returns:
            OrderBook: книга заявок.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'instruments/{symbol}/orderbook', params={'symbol': symbol})
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'instruments/{symbol}/orderbook', params={'symbol': symbol})

        if response.status_code == 200:
            return OrderBook.from_rest_dict(response.json())
        raise FinamResponseFailureException(response)
