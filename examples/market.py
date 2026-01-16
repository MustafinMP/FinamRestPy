import asyncio
import datetime

from finam_rest_py import Finam
from finam_rest_py.models import TimeFrame

FINAM_TOKEN = 'your_finam_token'
ACCOUNT_ID = 'your_account_id'


async def main():
    finam = await Finam.create(FINAM_TOKEN, ACCOUNT_ID)

    symbol = 'YDEX@MISX'

    print('Get bars example')
    now = datetime.datetime.now()
    bars = await finam.market.get_bars(symbol, TimeFrame.TIME_FRAME_H1, now - TimeFrame.TIME_FRAME_H1.max_deep(), now)
    for bar in bars:
        print(bar)

    print('Get last quote example')
    quote = await finam.market.get_last_quote(symbol)
    print(quote)

    print('Get latest trades example')
    trades = await finam.market.get_latest_trades(symbol)
    for trade in trades:
        print(trade)

    print('Get order book example')
    order_book = await finam.market.get_order_book(symbol)
    for row in order_book.orderbook:
        print(row)


if __name__ == "__main__":
    asyncio.run(main())
