from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class SessionSchema:
    type: str
    open_time: datetime
    close_time: datetime

    @classmethod
    def from_dict(cls, session_dict: dict) -> SessionSchema:
        return SessionSchema(
            type=session_dict['type'],
            open_time=datetime.strptime(session_dict['interval']['open_time'], "%Y-%m-%dT%H:%M:%SZ"),
            close_time=datetime.strptime(session_dict['interval']['close_time'], "%Y-%m-%dT%H:%M:%SZ")
        )
