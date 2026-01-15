from finam_rest_py import Finam
from finam_rest_py.models import Order, TradeSide, OrderType, OrderTypeInForce

FINAM_TOKEN = 'your_finam_token'
ACCOUNT_ID = 'your_account_id'

finam = Finam(FINAM_TOKEN, ACCOUNT_ID)

symbol = 'FMMM@MISX'

print('Place order example')
order = Order(
    account_id=ACCOUNT_ID,
    symbol=symbol,
    quantity=1,
    side=TradeSide.LONG,
    type=OrderType.ORDER_TYPE_MARKET,
    time_in_force=OrderTypeInForce.TIME_IN_FORCE_DAY
)

executed_order = finam.orders.place_order(order)
print(executed_order)

print('Get order example')
order = finam.orders.get_order(executed_order.order_id)
print(order)

print('Delete order example')

order = Order(
    account_id=ACCOUNT_ID,
    symbol=symbol,
    quantity=1,
    side=TradeSide.LONG,
    type=OrderType.ORDER_TYPE_LIMIT,
    time_in_force=OrderTypeInForce.TIME_IN_FORCE_DAY,
    limit_price=12  # заниженная цена покупки, чтобы сделка не исполнилась
)

no_executed_order = finam.orders.place_order(order)
print(no_executed_order)
no_executed_order = finam.orders.cancel_order(no_executed_order.order_id)
print(no_executed_order)

print('Get orders example')
orders = finam.orders.get_orders()
print(orders)