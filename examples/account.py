import datetime

from finam_rest_py import Finam

FINAM_TOKEN = 'your_finam_token'
ACCOUNT_ID = 'your_account_id'

finam = Finam(FINAM_TOKEN, ACCOUNT_ID)

print('Get account example')
account = finam.account.get_account()
print(account)

print('Get trades example')
trades = finam.account.get_trades(datetime.datetime.now(), limit=20)
for trade in trades:
    print(trade)

print('Get transactions example')
transactions = finam.account.transactions(datetime.datetime.now(), limit=20)
for transaction in transactions:
    print(transaction)