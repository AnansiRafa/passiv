from django.contrib import admin
from .models import CryptoAsset, CryptoPrice

@admin.register(CryptoAsset)
class CryptoAssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'market_cap_rank']

@admin.register(CryptoPrice)
class CryptoPriceAdmin(admin.ModelAdmin):
    list_display = ['asset', 'price_usd', 'market_cap', 'fetched_at']
