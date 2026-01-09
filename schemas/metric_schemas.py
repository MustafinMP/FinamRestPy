from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from schemas.converters import formatted_datetime


@dataclass
class QuotaUsageSchema:
    name: str
    limit: int
    remaining: int
    reset_time: datetime

    @classmethod
    def from_dict(cls, quota_usage_dict: dict) -> QuotaUsageSchema:
        return QuotaUsageSchema(
            name=quota_usage_dict['name'],
            limit=int(quota_usage_dict['limit']),
            remaining=int(quota_usage_dict['remaining']),
            reset_time=formatted_datetime(quota_usage_dict['reset_time'])
        )


@dataclass
class QuotaUsageMetricsSchema:
    quotas: list[QuotaUsageSchema]

    @classmethod
    def from_dict(cls, quota_usage_metrics_dict: dict) -> QuotaUsageMetricsSchema:
        return QuotaUsageMetricsSchema(
            quotas=[QuotaUsageSchema.from_dict(q) for q in quota_usage_metrics_dict['quotas']]
        )
