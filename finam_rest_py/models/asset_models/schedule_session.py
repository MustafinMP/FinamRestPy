from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from finam_rest_py.models.converters import formatted_datetime


@dataclass
class ScheduleSession:
    type: str
    open_time: datetime
    close_time: datetime

    @property
    def duration(self) -> timedelta:
        return self.close_time - self.open_time

    def now(self) -> bool:
        return self.open_time <= datetime.now() <= self.close_time

    @classmethod
    def from_dict(cls, session_dict: dict) -> ScheduleSession:
        return ScheduleSession(
            type=session_dict['type'],
            open_time=formatted_datetime(session_dict['interval']['start_time']),
            close_time=formatted_datetime(session_dict['interval']['end_time'])
        )
