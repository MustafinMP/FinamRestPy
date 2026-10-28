from datetime import timedelta, date

from finam_rest_py.models.corporation.bond_events import BondEvent, BondCouponEvent
from finam_rest_py.models.corporation.dividend import Dividend


async def test_get_future_dividends(finam_client):
    symbol = 'SBER@MISX'
    dividends = await finam_client.corporation.get_future_dividends(symbol)
    today = date.today()
    for d in dividends:
        assert isinstance(d, Dividend)
        assert d.date >= today


async def test_get_past_dividends(finam_client):
    symbol = 'SBER@MISX'
    today = date.today()
    start_date = today - timedelta(days=100)
    dividends = await finam_client.corporation.get_past_dividends(symbol, start_date, today - timedelta(days=1))
    for d in dividends:
        assert isinstance(d, Dividend)
        assert d.date < today


async def test_get_future_bond_events(finam_client):
    symbol = 'SU26250RMFS9@MISX'
    today = date.today()
    end_date = today + timedelta(days=200)
    events = await finam_client.corporation.get_future_bonds_events(symbol, today, end_date)
    for e in events:
        assert isinstance(e, BondEvent)
        assert e.date >= today


async def test_get_past_bond_events(finam_client):
    symbol = 'SU26250RMFS9@MISX'
    today = date.today()
    start_date = today - timedelta(days=200)
    events = await finam_client.corporation.get_past_bonds_events(symbol, start_date, today - timedelta(days=1))
    for e in events:
        assert isinstance(e, BondEvent)
        assert e.date < today


async def test_get_future_coupons(finam_client):
    symbol = 'SU26250RMFS9@MISX'
    today = date.today()
    end_date = today + timedelta(days=200)
    events = await finam_client.corporation.get_future_coupons(symbol, today, end_date)
    for e in events:
        assert isinstance(e, BondCouponEvent)
        assert e.date >= today


async def test_get_past_coupons(finam_client):
    symbol = 'SU26250RMFS9@MISX'
    today = date.today()
    start_date = today - timedelta(days=200)
    events = await finam_client.corporation.get_past_coupons(symbol, start_date, today - timedelta(days=1))
    for e in events:
        assert isinstance(e, BondCouponEvent)
        assert e.date < today
