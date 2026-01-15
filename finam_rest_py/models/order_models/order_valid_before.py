from __future__ import annotations

from enum import Enum


class OrderValidBefore(Enum):
    VALID_BEFORE_UNSPECIFIED = 0  # Значение не указано
    VALID_BEFORE_END_OF_DAY = 1  # До конца торгового дня
    VALID_BEFORE_GOOD_TILL_CANCEL = 2  # До отмены
    VALID_BEFORE_GOOD_TILL_DATE = 3  # До указанной даты - времени. Данный тип на текущий момент не поддерживается при выставлении заявки

    @classmethod
    def from_str(cls, string: str) -> OrderValidBefore:
        match string:
            case 'VALID_BEFORE_UNSPECIFIED':
                return cls.VALID_BEFORE_UNSPECIFIED
            case 'VALID_BEFORE_END_OF_DAY':
                return cls.VALID_BEFORE_END_OF_DAY
            case 'VALID_BEFORE_GOOD_TILL_CANCEL':
                return cls.VALID_BEFORE_GOOD_TILL_CANCEL
            case 'VALID_BEFORE_GOOD_TILL_DATE':
                return cls.VALID_BEFORE_GOOD_TILL_DATE
            case _:
                return cls.VALID_BEFORE_UNSPECIFIED
