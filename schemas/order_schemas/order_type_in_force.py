from __future__ import annotations

from enum import Enum


class OrderTypeInForce(Enum):
    TIME_IN_FORCE_UNSPECIFIED = 0  # Значение не указано
    TIME_IN_FORCE_DAY = 1  # До конца дня
    TIME_IN_FORCE_GOOD_TILL_CANCEL = 2  # Действителен до отмены
    TIME_IN_FORCE_GOOD_TILL_CROSSING = 3  # Действителен до пересечения
    TIME_IN_FORCE_EXT = 4  # Внебиржевая торговля
    TIME_IN_FORCE_ON_OPEN = 5  # На открытии биржи
    TIME_IN_FORCE_ON_CLOSE = 6  # На закрытии биржи
    TIME_IN_FORCE_IOC = 7  # Исполнить немедленно или отменить
    TIME_IN_FORCE_FOK = 8  # Исполнить полностью или отменить

    @classmethod
    def from_str(cls, string: str) -> OrderTypeInForce:
        match string:
            case 'TIME_IN_FORCE_UNSPECIFIED', _:
                return cls.TIME_IN_FORCE_UNSPECIFIED
            case 'TIME_IN_FORCE_DAY':
                return cls.TIME_IN_FORCE_DAY
            case 'TIME_IN_FORCE_GOOD_TILL_CANCEL':
                return cls.TIME_IN_FORCE_GOOD_TILL_CANCEL
            case 'TIME_IN_FORCE_GOOD_TILL_CROSSING':
                return cls.TIME_IN_FORCE_GOOD_TILL_CROSSING
            case 'TIME_IN_FORCE_EXT':
                return cls.TIME_IN_FORCE_EXT
            case 'TIME_IN_FORCE_ON_OPEN':
                return cls.TIME_IN_FORCE_ON_OPEN
            case 'TIME_IN_FORCE_ON_CLOSE':
                return cls.TIME_IN_FORCE_ON_CLOSE
            case 'TIME_IN_FORCE_IOC':
                return cls.TIME_IN_FORCE_IOC
            case 'TIME_IN_FORCE_FOK':
                return cls.TIME_IN_FORCE_FOK
            case _:
                return cls.TIME_IN_FORCE_UNSPECIFIED
