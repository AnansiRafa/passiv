from django.conf import settings
from datetime import datetime
from .models import InvestmentOpportunity, StockPrice
import yfinance as yf


def create_investment_opportunity(
    ticker: str, name: str, description: str
) -> InvestmentOpportunity:
    """Create a new or retrieve an existing InvestmentOpportunity."""
    obj, _ = InvestmentOpportunity.objects.get_or_create(
        ticker=ticker, defaults={"opportunity_name": name, "description": description}
    )
    return obj


def analyze_investment(opportunity: InvestmentOpportunity) -> dict:
    """
    Analyze an investment opportunity.
    This is a placeholder for real analysis logic.
    """
    return {"mock_score": 0.7, "risk": "moderate", "trend": "stable"}


def fetch_and_store_stock_prices(ticker_symbol: str, opportunity: InvestmentOpportunity):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="3mo")  # Use 'max' for full history

    for index, row in hist.iterrows():
        date = index.date()
        StockPrice.objects.update_or_create(
            opportunity=opportunity,
            date=date,
            defaults={
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"]
            }
        )