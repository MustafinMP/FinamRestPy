from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from finam_rest.schemas.account_schemas import AccountTradeSchema
from finam_rest.schemas.converters import formatted_datetime
from finam_rest.schemas.money_schema import MoneySchema


class TransactionCategory(Enum):
    OTHERS = 0  # Прочее
    DEPOSIT = 1  # Ввод ДС
    WITHDRAW = 2  # Вывод ДС
    INCOME = 5  # Доход
    COMMISSION = 7  # Комиссия
    TAX = 8  # Налог
    INHERITANCE = 9  # Наследство
    TRANSFER = 11  # Перевод ДС
    CONTRACT_TERMINATION = 12  # Расторжение договора
    OUTCOMES = 13  # Расходы
    FINE = 15  # Штраф
    LOAN = 19  # Займ

    @classmethod
    def from_str(cls, string: str) -> TransactionCategory:
        match string:
            case 'OTHERS': return cls.OTHERS
            case 'DEPOSIT': return cls.DEPOSIT
            case 'WITHDRAW': return cls.WITHDRAW
            case 'INCOME': return cls.INCOME
            case 'COMMISSION': return cls.COMMISSION
            case 'TAX': return cls.TAX
            case 'INHERITANCE': return cls.INHERITANCE
            case 'TRANSFER': return cls.TRANSFER
            case 'CONTRACT_TERMINATION': return cls.CONTRACT_TERMINATION
            case 'OUTCOMES': return cls.OUTCOMES
            case 'FINE': return cls.FINE
            case 'LOAN': return cls.LOAN
            case _: return cls.OTHERS


@dataclass
class TransactionSchema:
    id: str
    category: TransactionCategory
    timestamp: datetime
    symbol: str
    change: MoneySchema
    trade: Optional[AccountTradeSchema, None]
    transaction_category: TransactionCategory
    transaction_name: str
    change_qty: Optional[float, None]

    @classmethod
    def from_dict(cls, transaction: dict) -> TransactionSchema:
        return TransactionSchema(
            id=transaction['id'],
            category=TransactionCategory.from_str(transaction['category']),
            timestamp=formatted_datetime(transaction['timestamp']),
            symbol=transaction['symbol'],
            change=MoneySchema.from_dict(transaction['change']),
            trade=AccountTradeSchema.from_dict(transaction['trade']) if 'trade' in transaction.keys() else None,
            transaction_category=TransactionCategory.from_str(transaction['transaction_category']),
            transaction_name=transaction['transaction_name'],
            change_qty=float(transaction['change_qty']) if 'change_qty' in transaction.keys() else None
        )
