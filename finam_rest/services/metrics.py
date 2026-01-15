import requests

from finam_rest.services.base_service import BaseService
from finam_rest.models import QuotaUsageMetrics


class MetricsService(BaseService):
    def get_last_quote(self) -> QuotaUsageMetrics:
        url = f'{self._base_url}usage'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return QuotaUsageMetrics.from_dict(response.json())
        return None
