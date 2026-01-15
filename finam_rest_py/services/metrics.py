import requests

from finam_rest_py.exceptions import ResponseFailureException
from finam_rest_py.services.base_service import BaseService
from finam_rest_py.models import QuotaUsageMetrics


class MetricsService(BaseService):
    def get_usage_metrics(self) -> QuotaUsageMetrics:
        url = f'{self._base_url}usage'
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return QuotaUsageMetrics.from_dict(response.json())
        raise ResponseFailureException
