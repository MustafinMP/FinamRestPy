import asyncio

from finam_rest_py import Finam

FINAM_TOKEN = 'your_finam_token'
ACCOUNT_ID = 'your_account_id'


async def main():
    finam = await Finam.create(FINAM_TOKEN, ACCOUNT_ID)

    print('get usage metrics example')
    metrics = await finam.metrics.get_usage_metrics()
    for metric in metrics.quotas:
        print(metric)


if __name__ == "__main__":
    asyncio.run(main())
