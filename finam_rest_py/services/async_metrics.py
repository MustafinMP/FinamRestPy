from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.models import QuotaUsageMetrics
from finam_rest_py.services.async_base_service import AsyncBaseService


class MetricsService(AsyncBaseService):
    async def get_usage_metrics(self) -> QuotaUsageMetrics:
        async with self._session.get(f'usage') as response:
            if response.status == 200:
                return QuotaUsageMetrics.from_dict(await response.json())
            raise ResponseFailureException
