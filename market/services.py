# market/services.py

import pytz
from datetime import datetime
from .models import MarketStatusUpdate

MARKET_TIMES = {
    "pre_market_start": (4, 0),
    "market_open": (9, 30),
    "market_close": (16, 0),
    "after_hours_end": (20, 0),
}


def get_market_status() -> str:
    eastern = pytz.timezone("US/Eastern")
    now = datetime.now(eastern)

    if now.weekday() >= 5:
        return "closed"

    t = now.time()
    if (
        t >= datetime.strptime("04:00", "%H:%M").time()
        and t < datetime.strptime("09:30", "%H:%M").time()
    ):
        return "closed"
    if (
        t >= datetime.strptime("09:30", "%H:%M").time()
        and t < datetime.strptime("16:00", "%H:%M").time()
    ):
        return "open"
    if (
        t >= datetime.strptime("16:00", "%H:%M").time()
        and t < datetime.strptime("20:00", "%H:%M").time()
    ):
        return "closed"
    return "closed"


def record_market_status() -> MarketStatusUpdate:
    status = get_market_status()
    return MarketStatusUpdate.objects.create(status=status)


def is_market_open() -> bool:
    return get_market_status() == "open"
