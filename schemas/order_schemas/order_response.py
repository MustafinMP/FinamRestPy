from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from schemas.order_schemas.order import OrderSchema


@dataclass
class OrderResponse:
    order_id: str
    exec_id: str
    status: None
    order: OrderSchema
    transact_at: datetime

    @classmethod
    def from_dict(cls, order_dict: dict) -> OrderResponse:
        return OrderResponse(
            order_id=order_dict['order_id'],
            exec_id=order_dict['exec_id'],
            status=order_dict['order_status'],
            order=OrderSchema.from_dict(order_dict['order_schemas']),
            transact_at=datetime.strptime(order_dict['transact_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        )
