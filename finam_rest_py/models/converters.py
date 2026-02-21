from datetime import datetime, timezone, timedelta


def date_from_dict(date_dict: dict) -> datetime:
    return datetime(year=date_dict['year'], month=date_dict['month'], day=date_dict['day'])


def formatted_datetime(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp.replace('Z', '+00:00')).astimezone().replace(tzinfo=None)
