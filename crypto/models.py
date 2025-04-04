from django.db import models

class CryptoAsset(models.Model):
    coingecko_id = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)
    market_cap_rank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.symbol.upper()})"


class CryptoPrice(models.Model):
    asset = models.ForeignKey(CryptoAsset, on_delete=models.CASCADE, related_name='prices')
    price_usd = models.DecimalField(max_digits=20, decimal_places=10)
    market_cap = models.BigIntegerField(null=True, blank=True)
    volume_24h = models.BigIntegerField(null=True, blank=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fetched_at']
