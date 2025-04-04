# investment/models.py
from django.db import models


SOURCE_CHOICES = [
    ('stock', 'Stock'),
    ('crypto', 'Crypto'),
]

class InvestmentOpportunity(models.Model):
    ticker = models.CharField(max_length=10)
    opportunity_name = models.CharField(max_length=255)
    description = models.TextField()
    data = models.JSONField(default=dict)  # Additional analysis results, metrics, etc.
    source_type = models.CharField(
    max_length=10,
    choices=SOURCE_CHOICES,
    default='stock'
    )

    def __str__(self):
        return f"{self.ticker}: {self.opportunity_name}"

class StockPrice(models.Model):
    opportunity = models.ForeignKey(
        InvestmentOpportunity,
        on_delete=models.CASCADE,
        related_name='stock_prices'
    )
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('opportunity', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.opportunity.ticker} - {self.date} - Close: {self.close}"