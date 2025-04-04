import requests
from django.utils.timezone import now
from .models import CryptoAsset, CryptoPrice

COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"

def fetch_top_crypto_assets(limit=10):
    url = f"{COINGECKO_API_BASE}/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def ingest_top_crypto_assets(limit=10):
    data = fetch_top_crypto_assets(limit=limit)
    for entry in data:
        asset, _ = CryptoAsset.objects.update_or_create(
            coingecko_id=entry["id"],
            defaults={
                "name": entry["name"],
                "symbol": entry["symbol"],
                "image": entry.get("image"),
                "market_cap_rank": entry.get("market_cap_rank")
            }
        )
        CryptoPrice.objects.create(
            asset=asset,
            price_usd=entry.get("current_price"),
            market_cap=entry.get("market_cap"),
            volume_24h=entry.get("total_volume"),
            fetched_at=now()
        )
