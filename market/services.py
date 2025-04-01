# passiv/market/services.py

import pytz
from datetime import datetime
from .models import MarketStatusUpdate


def get_market_status():
    """
    Determines the current market status based on US/Eastern time.
    Returns one of: "open", "closed", "pre_market", or "after_hours".
    """
    # Use the US/Eastern timezone for market hours
    eastern = pytz.timezone("US/Eastern")
    now = datetime.now(eastern)

    # If today is Saturday (5) or Sunday (6), the market is closed.
    if now.weekday() >= 5:
        return "closed"

    # Define market open and close times using today's date
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)

    if market_open <= now < market_close:
        return "open"

    # For simplicity, we're returning "closed" outside of market hours.
    # You could extend this logic to return "pre_market" or "after_hours" if needed.
    return "closed"


def record_market_status():
    """
    Fetches the current market status and creates a record in the database.
    This function writes a new entry to the MarketStatusUpdate model,
    capturing the status and timestamp.
    """
    status = get_market_status()
    update = MarketStatusUpdate.objects.create(status=status)
    return update
