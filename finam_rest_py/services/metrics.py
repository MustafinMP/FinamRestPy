from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.models import QuotaUsageMetrics
from finam_rest_py.services.base_service import AsyncBaseService


class MetricsService(AsyncBaseService):
    async def get_usage_metrics(self) -> QuotaUsageMetrics:
        response = await self._session.get(f'usage')
        if response.status_code == 200:
            return QuotaUsageMetrics.from_dict(response.json())
        raise ResponseFailureException
