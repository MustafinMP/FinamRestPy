from __future__ import annotations

from enum import Enum


class TimeFrame(Enum):
    TIME_FRAME_UNSPECIFIED = 0  # Таймфрейм не указан
    TIME_FRAME_M1 = 1  # 1 минута. Глубина данных 7 дней.
    TIME_FRAME_M5 = 5  # 5 минут. Глубина данных 30 дней.
    TIME_FRAME_M15 = 9  # 15 минут. Глубина данных 30 дней.
    TIME_FRAME_M30 = 11  # 30 минут. Глубина данных 30 дней.
    TIME_FRAME_H1 = 12 # 1 час. Глубина данных 30 дней.
    TIME_FRAME_H2 = 13  # 2 часа. Глубина данных 30 дней.
    TIME_FRAME_H4 = 15  # 4 часа. Глубина данных 30 дней.
    TIME_FRAME_H8 = 17  # 8 часов. Глубина данных 30 дней.
    TIME_FRAME_D = 19  # День. Глубина данных 365 дней.
    TIME_FRAME_W = 20  # Неделя. Глубина данных 365 * 5 дней.
    TIME_FRAME_MN = 21  # Месяц. Глубина данных 365 * 5 дней.
    TIME_FRAME_QR = 22  # Квартал. Глубина данных 365 * 5 дней.

    @classmethod
    def from_str(cls, string: str) -> TimeFrame:
        match string:
            case 'TIME_FRAME_UNSPECIFIED': return cls.TIME_FRAME_UNSPECIFIED
            case 'TIME_FRAME_M1': return cls.TIME_FRAME_M1
            case 'TIME_FRAME_M5': return cls.TIME_FRAME_M5
            case 'TIME_FRAME_M15': return cls.TIME_FRAME_M15
            case 'TIME_FRAME_M30': return cls.TIME_FRAME_M30
            case 'TIME_FRAME_H1': return cls.TIME_FRAME_H1
            case 'TIME_FRAME_H2': return cls.TIME_FRAME_H2
            case 'TIME_FRAME_H4': return cls.TIME_FRAME_H4
            case 'TIME_FRAME_H8': return cls.TIME_FRAME_H8
            case 'TIME_FRAME_D': return cls.TIME_FRAME_D
            case 'TIME_FRAME_W': return cls.TIME_FRAME_W
            case 'TIME_FRAME_MN': return cls.TIME_FRAME_MN
            case 'TIME_FRAME_QR': return cls.TIME_FRAME_QR
            case _: return cls.TIME_FRAME_UNSPECIFIED
