from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from finam_rest.models.converters import formatted_datetime


@dataclass
class ScheduleSession:
    type: str
    open_time: datetime
    close_time: datetime

    @classmethod
    def from_dict(cls, session_dict: dict) -> ScheduleSession:
        print(session_dict)
        return ScheduleSession(
            type=session_dict['type'],
            open_time=formatted_datetime(session_dict['interval']['start_time']),
            close_time=formatted_datetime(session_dict['interval']['end_time'])
        )
