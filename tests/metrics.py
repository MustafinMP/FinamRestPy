import datetime

from config import FINAM_TOKEN, ACCOUNT_ID
from finam_rest.finam import Finam

finam = Finam(FINAM_TOKEN, ACCOUNT_ID)
print('get last quote')
print(finam.metrics.get_last_quote())