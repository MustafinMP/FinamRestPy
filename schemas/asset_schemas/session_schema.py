from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from schemas.converters import formatted_datetime


@dataclass
class SessionSchema:
    type: str
    open_time: datetime
    close_time: datetime

    @classmethod
    def from_dict(cls, session_dict: dict) -> SessionSchema:
        return SessionSchema(
            type=session_dict['type'],
            open_time=formatted_datetime(session_dict['interval']['open_time']),
            close_time=formatted_datetime(session_dict['interval']['close_time'])
        )
