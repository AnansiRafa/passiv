from django.db import models


class MarketStatusUpdate(models.Model):
    OPEN = "open"
    CLOSED = "closed"
    PRE_MARKET = "pre_market"
    AFTER_HOURS = "after_hours"

    MARKET_CHOICES = [
        (OPEN, "Open"),
        (CLOSED, "Closed"),
        (PRE_MARKET, "Pre-market"),
        (AFTER_HOURS, "After Hours"),
    ]

    status = models.CharField(max_length=20, choices=MARKET_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_status_display()} at {self.timestamp}"
