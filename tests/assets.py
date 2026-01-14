import datetime

from config import FINAM_TOKEN, ACCOUNT_ID
from finam_rest.finam import Finam
from finam_rest.schemas.market_schemas import TimeFrame
# 'YDEX@MISX'
finam = Finam(FINAM_TOKEN, ACCOUNT_ID)
print('get assets')
print(finam.instruments.get_assets())
print('get clock')
print(finam.instruments.get_clock())
print('get exchanges')
print(finam.instruments.get_exchanges())
print('get asset')
print(finam.instruments.get_asset('YDEX@MISX'))
print('get asset params')
print(finam.instruments.get_asset_params('YDEX@MISX', finam._account_id))
print('get option chain')
print(finam.instruments.get_options_chain('YDEX@MISX'))