from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class ConvertationType(Enum):
    CONVTYPE_UNKNOWN = 'CONVTYPE_UNKNOWN'
    BUYBACK = 'BUYBACK'
    CALL_OPTION_EXERCISED = 'CALL_OPTION_EXERCISED'
    DRAWINGS = 'DRAWINGS'
    DRAWINGS_BY_LOTTERY = 'DRAWINGS_BY_LOTTERY'
    EARLY_CONVERSION = 'EARLY_CONVERSION'
    MATURITY = 'MATURITY'
    ORDINARY = 'ORDINARY'
    PUT_OPTION_EXERCISED = 'PUT_OPTION_EXERCISED'
    TENDER_OFFER = 'TENDER_OFFER'

    @classmethod
    def from_str(cls, str_value: str) -> ConvertationType:
        return {
            'CONVTYPE_UNKNOWN': cls.CONVTYPE_UNKNOWN,
            'BUYBACK': cls.BUYBACK,
            'CALL_OPTION_EXERCISED': cls.CALL_OPTION_EXERCISED,
            'DRAWINGS': cls.DRAWINGS,
            'DRAWINGS_BY_LOTTERY': cls.DRAWINGS_BY_LOTTERY,
            'EARLY_CONVERSION': cls.EARLY_CONVERSION,
            'MATURITY': cls.MATURITY,
            'ORDINARY': cls.ORDINARY,
            'PUT_OPTION_EXERCISED': cls.PUT_OPTION_EXERCISED,
            'TENDER_OFFER': cls.TENDER_OFFER,
        }.get(str_value, cls.CONVTYPE_UNKNOWN)


@dataclass
class Split:
    exec_date: date
    old_ratio: float
    new_ratio: float
    new_lot: float
    convertation_type: ConvertationType

    @classmethod
    def from_dict(cls, data: dict) -> Split:
        return Split(
            exec_date=date(
                year=data['exec_date']['year'],
                month=data['exec_date']['month'],
                day=data['exec_date']['day']
            ),
            old_ratio=float(data['old_ratio']['value']),
            new_ratio=float(data['new_ratio']['value']),
            new_lot=float(data['new_lot']['value']),
            convertation_type=ConvertationType.from_str(data['convertation_type'])
        )
