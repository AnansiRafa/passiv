# content/models.py
from django.db import models
from investment.models import InvestmentOpportunity


class ContentVersion(models.Model):
    opportunity = models.ForeignKey(
        InvestmentOpportunity,
        null=True,
        on_delete=models.CASCADE,
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
        return f"{self.content_id} v{self.version}"
