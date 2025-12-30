import requests

from _services.base_service import BaseService
from schemas.metric_schemas import QuotaUsageMetricsSchema


class MetricsService(BaseService):
    def get_last_quote(self) -> QuotaUsageMetricsSchema:
        url = f'{self._base_url}usage'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return QuotaUsageMetricsSchema.from_dict(response.json())
        return None
