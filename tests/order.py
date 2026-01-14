import datetime

from config import FINAM_TOKEN, ACCOUNT_ID
from finam_rest.finam import Finam
from finam_rest.schemas.market_schemas import TimeFrame
from finam_rest.schemas.order_schemas import OrderSchema, OrderType, OrderTypeInForce
from finam_rest.schemas.trade_side import TradeSide

# 'YDEX@MISX'
finam = Finam(FINAM_TOKEN, ACCOUNT_ID)
print('get orders')
orders = finam.orders.get_orders()
print(orders)

order = OrderSchema(
    account_id=ACCOUNT_ID,
    symbol='FMMM@MISX',
    quantity=1,
    side=TradeSide.LONG,
    type=OrderType.ORDER_TYPE_MARKET,
    time_in_force=OrderTypeInForce.TIME_IN_FORCE_DAY
)

print('place order')
answer = finam.orders.place_order(order)
print(answer)

print('get order')
answer = finam.orders.get_order(answer.order_id)
print(answer)

order = OrderSchema(
    account_id=ACCOUNT_ID,
    symbol='FMMM@MISX',
    quantity=1,
    side=TradeSide.LONG,
    type=OrderType.ORDER_TYPE_LIMIT,
    time_in_force=OrderTypeInForce.TIME_IN_FORCE_DAY,
    limit_price=12
)

print('delete order')
answer = finam.orders.place_order(order)
print(answer)
answer = finam.orders.cancel_order(answer.order_id)
print(answer)
