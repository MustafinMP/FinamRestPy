from finam_rest_py import Finam

FINAM_TOKEN = 'your_finam_token'
ACCOUNT_ID = 'your_account_id'

finam = Finam(FINAM_TOKEN, ACCOUNT_ID)

print('get usage metrics example')
metrics = finam.metrics.get_usage_metrics()
for metric in metrics.quotas:
    print(metric)