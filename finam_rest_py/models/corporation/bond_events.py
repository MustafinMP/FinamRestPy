from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class BondEvent:
    date: date


@dataclass
class BondCouponEvent(BondEvent):
    record_date: date | None
    start_date: date | None
    face_value: float
    value_percent: float
    value: float

    @classmethod
    def from_dict(cls, data: dict) -> BondCouponEvent:
        details = data['coupon_details']
        return BondCouponEvent(
            date=date(year=data['date']['year'], month=data['date']['month'], day=data['date']['day']),
            start_date=date(year=details['start_date']['year'], month=details['start_date']['month'],
                            day=details['start_date']['day']) if details['start_date']['year'] != 0 else None,
            record_date=date(year=details['record_date']['year'], month=details['record_date']['month'],
                             day=details['record_date']['day']) if details['record_date']['year'] != 0 else None,
            face_value=float(details['face_value']['value']),
            value_percent=float(details['value_percent']['value']),
            value=float(data['value']['value']),
        )


@dataclass
class BondAmortizationEvent(BondEvent):
    initial_face_value: float
    new_face_value: float
    amortization_percent: float
    value: float

    @classmethod
    def from_dict(cls, data: dict) -> BondAmortizationEvent:
        details = data['amortization_details']
        return BondAmortizationEvent(
            date=date(year=data['date']['year'], month=data['date']['month'], day=data['date']['day']),
            initial_face_value=float(details['initial_face_value']['value']),
            new_face_value=float(details['new_face_value']['value']),
            amortization_percent=float(details['amortization_percent']['value']),
            value=float(data['value']['value']),
        )


@dataclass
class BondOfferEvent(BondEvent):
    offer_type: str
    price: float
    start_date: date | None
    end_date: date | None

    @classmethod
    def from_dict(cls, data: dict) -> BondOfferEvent:
        details = data['offer_details']
        return BondOfferEvent(
            date=date(year=data['date']['year'], month=data['date']['month'], day=data['date']['day']),
            offer_type=details['offer_type'],
            price=float(details['price']['value']),
            start_date=date(year=details['start_date']['year'], month=details['start_date']['month'],
                            day=details['start_date']['day']) if details['start_date']['year'] != 0 else None,
            end_date=date(year=details['end_date']['year'], month=details['end_date']['month'],
                          day=details['end_date']['day']) if details['end_date']['year'] != 0 else None,
        )
