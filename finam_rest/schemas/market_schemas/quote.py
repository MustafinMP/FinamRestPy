from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from finam_rest.schemas.converters import formatted_datetime


@dataclass
class QuoteOptionSchema:
    open_interest: float  # Открытый интерес
    implied_volatility: float  # Подразумеваемая волатильность
    theoretical_price: float  # Теоретическая цена
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float

    @classmethod
    def from_dict(cls, option_dict: dict) -> QuoteOptionSchema:
        return QuoteOptionSchema(
            open_interest=float(option_dict['open_interest']['value']),
            implied_volatility=float(option_dict['implied_volatility']['value']),
            theoretical_price=float(option_dict['theoretical_price']['value']),
            delta=float(option_dict['delta']['value']),
            gamma=float(option_dict['gamma']['value']),
            theta=float(option_dict['theta']['value']),
            vega=float(option_dict['vega']['value']),
            rho=float(option_dict['rho']['value']),
        )


@dataclass
class QuoteSchema:
    symbol: str
    timestamp: datetime
    ask: float  # Аск. 0 при отсутствии активного аска
    ask_size: float  # Размер аска
    bid: float  # Бид. 0 при отсутствии активного бида
    bid_size: float  # Размер бида
    last: float  # Цена последней сделки
    last_size: float  # Размер последней сделки
    volume: float  # Дневной объем сделок
    turnover: float  # Дневной оборот сделок
    open: float  # Цена открытия. Дневная
    high: float  # Максимальная цена. Дневная
    low: float  # Минимальная цена. Дневная
    close: float  # Цена закрытия. Дневная
    change: float  # Изменение цены (last минус close)
    option: Optional[QuoteOptionSchema | None]  # Информация об опционе

    @classmethod
    def from_dict(cls, quote_dict: dict) -> QuoteSchema:
        quote = quote_dict['quote']
        return QuoteSchema(
            symbol=quote_dict['symbol'],
            timestamp=formatted_datetime(quote['timestamp']),
            ask=float(quote['ask']['value']),
            ask_size=float(quote['ask_size']['value']),
            bid=float(quote['bid']['value']),
            bid_size=float(quote['bid_size']['value']),
            last=float(quote['last']['value']),
            last_size=float(quote['last_size']['value']),
            volume=float(quote['volume']['value']),
            turnover=float(quote['turnover']['value']),
            open=float(quote['open']['value']),
            high=float(quote['high']['value']),
            low=float(quote['low']['value']),
            close=float(quote['close']['value']),
            change=float(quote['change']['value']),
            option=QuoteOptionSchema.from_dict(quote['option']) if 'option' in quote.keys() else None
        )
