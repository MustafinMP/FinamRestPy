from datetime import datetime

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Account, AssetTrade, Transaction
from finam_rest_py.services.base_service import AsyncBaseService


class AccountService(AsyncBaseService):
    async def get_account(self) -> Account:
        """Получает аккаунт в Finam.

        Returns:
            Account: аккаунт в Finam.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'accounts/{self._account_id}')
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'accounts/{self._account_id}')
        if response.status_code == 200:
            return Account.from_dict(response.json())
        raise FinamResponseFailureException(response)

    async def get_trades(self,
                         end_time: datetime,
                         start_time: datetime | None = None,
                         limit: int | None = None) -> list[AssetTrade]:
        """Получает истории по сделкам аккаунта.

        Args:
            end_time (datetime): конец запрашиваемого периода.
            start_time (Optional[datetime]): начало запрашиваемого периода.
            limit (Optional[int]): лимит количества сделок.

        Returns:
            list[Trade]: список сделок по аккаунту.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        params: dict[str, str | int] = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = await self._session.get(f'accounts/{self._account_id}/trades', params=params)
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'accounts/{self._account_id}/trades', params=params)
        if response.status_code == 200:
            return [AssetTrade.from_dict(t) for t in response.json()['trades']]
        raise FinamResponseFailureException(response)

    async def get_transactions(self,
                               end_time: datetime,
                               start_time: datetime | None = None,
                               limit: int | None = None) -> list[Transaction]:
        """Получает список транзакций аккаунта.

        Args:
            end_time (datetime): конец запрашиваемого периода.
            start_time (Optional[datetime]): начало запрашиваемого периода.
            limit (Optional[int]): лимит количества транзакций.

        Returns:
            list[Transaction]: список транзакций аккаунта.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        params: dict[str, str | int] = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = await self._session.get(f'accounts/{self._account_id}/transactions', params=params)
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'accounts/{self._account_id}/transactions', params=params)
        if response.status_code == 200:
            return [Transaction.from_dict(t) for t in response.json()['transactions']]
        raise FinamResponseFailureException(response)
