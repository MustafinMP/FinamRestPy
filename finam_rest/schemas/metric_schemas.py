from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from finam_rest.schemas.converters import formatted_datetime


@dataclass
class QuotaUsageSchema:
    name: str
    limit: int
    remaining: int
    reset_time: Optional[datetime | None]

    @classmethod
    def from_dict(cls, quota_usage_dict: dict) -> QuotaUsageSchema:
        return QuotaUsageSchema(
            name=quota_usage_dict['name'],
            limit=int(quota_usage_dict['limit']),
            remaining=int(quota_usage_dict['remaining']),
            reset_time=formatted_datetime(quota_usage_dict['reset_time']) if 'reset_time' in quota_usage_dict else None
        )


@dataclass
class QuotaUsageMetricsSchema:
    quotas: list[QuotaUsageSchema]

    @classmethod
    def from_dict(cls, quota_usage_metrics_dict: dict) -> QuotaUsageMetricsSchema:
        return QuotaUsageMetricsSchema(
            quotas=[QuotaUsageSchema.from_dict(q) for q in quota_usage_metrics_dict['quotas']]
        )
