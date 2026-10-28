import os
from datetime import datetime

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Report
from finam_rest_py.services.base_service import AsyncBaseService


class ReportService(AsyncBaseService):
    async def init_report(self, date_begin: datetime, date_end: datetime, long_form: bool = False) -> str:
        """Инициирует формирование отчета на сервере

        Args:
            date_begin (datetime): левая граница периода отчета.
            date_end (datetime): правая граница периода отчета.
            long_form (bool): длинный формат отчета, по умолчанию False (короткий формат)

        Returns:
            str: ID отчета на сервере.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """

        params = {
            'date_range.date_begin': date_begin.isoformat() + 'Z',
            'date_range.date_end': date_end.isoformat() + 'Z',
            'report_form': 'REPORT_FORM_LONG' if long_form else 'REPORT_FORM_SHORT',
            'account_id': self._account_id
        }
        response = await self._session.post('report', params=params)
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.post('report', params=params)
        if response.status_code == 200:
            return response.json()['report_id']
        raise FinamResponseFailureException(response)

    async def get_report(self, report_id: str):
        response = await self._session.get(f'report/{report_id}/info')
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'report/{report_id}/info')
        if response.status_code == 200:
            return Report.from_dict(response.json())
        raise FinamResponseFailureException(response)


    async def load_report(self, report_id: str, save_dir: str = '', filename: str | None = None) -> bool:
        """Скачивает отчет в файл. Если отчет не готов (ссылка отсутствует), скачивание не происходит.

        Args:
            report_id (str): ID отчета на сервере.
            save_dir (str): директория, в которую нужно сохранить файл.
            filename (str | None): новое имя файла (по умолчанию имя файла = ID отчета)

        Returns:
            (bool): удалось ли скачивание (если отчет не готов, скачивание не произойдет).
        """
        report = await self.get_report(report_id)
        if report.url is not None:
            url = report.url
            response = await self._session.get(url, follow_redirects=True)
            response.raise_for_status()
            filename = filename + '.xls' if filename else url.split('/')[-1]
            file_path = os.path.join(save_dir, filename)
            with open(file_path, "wb") as file:
                async for chunk in response.aiter_bytes():
                    file.write(chunk)
            return True
        return False


    async def load_report_bytes(self, report_id: str) -> bytes | None:
        """Загружает отчет и возвращает его содержимое в виде байтов.
        Если отчет не готов (ссылка отсутствует), возвращает None.

        Args:
            report_id: ID отчета на сервере.

        Returns:
            Байты файла отчета или None, если отчет еще не готов.
        """
        report = await self.get_report(report_id)
        if report.url is not None:
            url = report.url
            response = await self._session.get(url, follow_redirects=True)
            response.raise_for_status()
            return await response.aread()

        return None