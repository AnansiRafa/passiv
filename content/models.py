# content/models.py
from django.db import models
from investment.models import InvestmentOpportunity
from crypto.models import CryptoAsset


class ContentVersion(models.Model):
    opportunity = models.ForeignKey(
        InvestmentOpportunity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="content_versions"
    )

    crypto_asset = models.ForeignKey(
        CryptoAsset,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="content_versions"
    )
    content_id = models.CharField(max_length=255)  # e.g., "inv_AAPL_20250331"
    version = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField(blank=True)
    metrics = models.JSONField(
        default=dict
    )  # Requires Django 3.1+ or PostgreSQL for earlier versions

    class Meta:
        unique_together = ("content_id", "version")
        ordering = ["-version"]

    def __str__(self):
        label = self.opportunity.ticker if self.opportunity else self.crypto_asset.symbol
        return f"{self.content_id} v{self.version} ({label})"
