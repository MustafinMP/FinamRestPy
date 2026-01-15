from finam_rest_py import Finam

FINAM_TOKEN = 'your_finam_token'
ACCOUNT_ID = 'your_account_id'

finam = Finam(FINAM_TOKEN, ACCOUNT_ID)
symbol = 'YDEX@MISX'

print('Get clock example')
clock = finam.instruments.get_clock()
print(clock)

print('Get exchanges example')
exchanges = finam.instruments.get_exchanges()
for exchange in exchanges:
    print(exchange)

print('Get asset example')
asset = finam.instruments.get_asset(symbol)
print(asset)

print('Get asset params example')
asset_params = finam.instruments.get_asset_params(symbol, ACCOUNT_ID)
print(asset_params)

print('Get option chain example')
chain = finam.instruments.get_options_chain(symbol)
for option in chain:
    print(option)

print('Get schedule example')
schedule = finam.instruments.get_schedule(symbol)
for session in schedule:
    print(session)