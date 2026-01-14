import datetime

from config import FINAM_TOKEN, ACCOUNT_ID
from finam_rest.finam import Finam
from finam_rest.schemas.market_schemas import TimeFrame

finam = Finam(FINAM_TOKEN, ACCOUNT_ID)
print('get bars')
print(finam.market.get_bars('YDEX@MISX', TimeFrame.TIME_FRAME_H1, datetime.datetime.now()))
print('get last quote')
print(finam.market.get_last_quote('YDEX@MISX'))
print('get latest trades')
print(finam.market.get_latest_trades('YDEX@MISX'))
print('get order book')
print(finam.market.get_order_book('YDEX@MISX'))