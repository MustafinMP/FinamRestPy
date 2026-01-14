import requests

from finam_rest._services.base_service import BaseService
from finam_rest.schemas.metric_schemas import QuotaUsageMetricsSchema


class MetricsService(BaseService):
    def get_last_quote(self) -> QuotaUsageMetricsSchema:
        url = f'{self._base_url}usage'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return QuotaUsageMetricsSchema.from_dict(response.json())
        return None
