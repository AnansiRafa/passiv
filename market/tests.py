# passiv/market/tests.py

from django.test import TestCase
from freezegun import freeze_time
from datetime import datetime
import pytz
from .services import get_market_status, record_market_status
from .models import MarketStatusUpdate


def get_aware_time(year, month, day, hour, minute, second):
    """
    Helper function to create a timezone-aware datetime object for US/Eastern.
    This ensures that DST rules are applied automatically.
    """
    eastern = pytz.timezone("US/Eastern")
    return eastern.localize(datetime(year, month, day, hour, minute, second))


class MarketStatusServiceTests(TestCase):

    @freeze_time(get_aware_time(2023, 4, 3, 10, 0, 0))
    def test_get_market_status_open(self):
        # Monday, April 3, 2023 at 10:00 AM Eastern should be within market hours.
        status = get_market_status()
        self.assertEqual(
            status, "open", "Market should be open at 10:00 AM on a weekday."
        )

    @freeze_time(get_aware_time(2023, 4, 3, 8, 0, 0))
    def test_get_market_status_closed_before_open(self):
        # Monday at 8:00 AM Eastern is before the market opens.
        status = get_market_status()
        self.assertEqual(
            status, "closed", "Market should be closed before opening time."
        )

    @freeze_time(get_aware_time(2023, 4, 3, 17, 0, 0))
    def test_get_market_status_closed_after_close(self):
        # Monday at 5:00 PM Eastern is after the market closes.
        status = get_market_status()
        self.assertEqual(
            status, "closed", "Market should be closed after market hours."
        )

    @freeze_time(get_aware_time(2023, 4, 1, 12, 0, 0))
    def test_get_market_status_closed_weekend(self):
        # Saturday at noon should result in a closed market.
        status = get_market_status()
        self.assertEqual(status, "closed", "Market should be closed on Saturday.")

    @freeze_time(get_aware_time(2023, 4, 2, 12, 0, 0))
    def test_get_market_status_closed_sunday(self):
        # Sunday at noon should result in a closed market.
        status = get_market_status()
        self.assertEqual(status, "closed", "Market should be closed on Sunday.")

    @freeze_time(get_aware_time(2023, 4, 3, 10, 0, 0))
    def test_record_market_status_creates_record(self):
        # Confirm that a new record is created when recording the market status.
        self.assertEqual(MarketStatusUpdate.objects.count(), 0)
        update = record_market_status()
        self.assertEqual(update.status, "open")
        self.assertEqual(MarketStatusUpdate.objects.count(), 1)
