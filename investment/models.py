# investment/models.py
from django.db import models


class InvestmentOpportunity(models.Model):
    ticker = models.CharField(max_length=10)
    opportunity_name = models.CharField(max_length=255)
    description = models.TextField()
    data = models.JSONField(default=dict)  # Additional analysis results, metrics, etc.

    def __str__(self):
        return f"{self.ticker}: {self.opportunity_name}"
