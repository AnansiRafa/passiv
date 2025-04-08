import pytest
from unittest import mock
from investment.models import InvestmentOpportunity, StockPrice
import investment.services as services
from investment.tasks import fetch_stock_price_history
from django.utils import timezone
from datetime import datetime
import pandas as pd

@pytest.mark.django_db
def test_create_investment_opportunity():
    opp = InvestmentOpportunity.objects.create(
        ticker='AAPL',
        opportunity_name='Apple Inc.',
        description='Tech company'
    )
    assert opp.ticker == 'AAPL'
    assert InvestmentOpportunity.objects.count() == 1

@pytest.mark.django_db
def test_create_stock_price():
    opp = InvestmentOpportunity.objects.create(ticker='GOOG', opportunity_name='Google')
    price = StockPrice.objects.create(
        opportunity=opp,
        date=timezone.now().date(),
        open=100.0,
        close=110.0,
        high=115.0,
        low=99.0,
        volume=1000000
    )
    assert price.opportunity.ticker == 'GOOG'
    assert StockPrice.objects.count() == 1

@pytest.mark.django_db
def test_fetch_and_store_stock_prices():
    opp = InvestmentOpportunity.objects.create(
        ticker='MSFT',
        opportunity_name='Microsoft',
        description='Software',
        source_type='stock'
    )

    mock_df = pd.DataFrame(
        data={
            'Open': [100.0],
            'Close': [110.0],
            'High': [115.0],
            'Low': [99.0],
            'Volume': [1000000],
        },
        index=[pd.Timestamp("2023-01-01")]
    )

    with mock.patch("investment.services.yf.Ticker") as MockTicker:
        instance = MockTicker.return_value
        instance.history.return_value = mock_df

        services.fetch_and_store_stock_prices(opp.ticker, opp)

    assert StockPrice.objects.filter(opportunity=opp).exists()

@pytest.mark.django_db
@mock.patch("investment.tasks.fetch_and_store_stock_prices")
def test_fetch_stock_price_history_task(mock_service):
    opp = InvestmentOpportunity.objects.create(ticker='TSLA', opportunity_name='Tesla')
    fetch_stock_price_history(opp.id)
    mock_service.assert_called_once()
