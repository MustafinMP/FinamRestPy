from datetime import datetime


def datetime_from_dict(date_dict: dict) -> datetime:
    return datetime(year=date_dict['year'], month=date_dict['month'], day=date_dict['day'])


def formatted_datetime(timestamp: str) -> datetime:
    try:
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
