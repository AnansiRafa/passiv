import pytest
from unittest import mock
from django.utils import timezone
from crypto.models import CryptoAsset, CryptoPrice
import crypto.services as services

@pytest.mark.django_db
def test_create_crypto_asset():
    asset = CryptoAsset.objects.create(
        coingecko_id="bitcoin",
        symbol="btc",
        name="Bitcoin",
        image="https://image.url/bitcoin.png",
        market_cap_rank=1
    )
    assert asset.symbol == "btc"
    assert CryptoAsset.objects.count() == 1

@pytest.mark.django_db
def test_create_crypto_price():
    asset = CryptoAsset.objects.create(coingecko_id="eth", symbol="eth", name="Ethereum")
    price = CryptoPrice.objects.create(
        asset=asset,
        price_usd=1800.00,
        market_cap=1000000000,
        volume_24h=50000000
    )
    assert price.asset.symbol == "eth"
    assert CryptoPrice.objects.count() == 1

@pytest.mark.django_db
@mock.patch("crypto.services.requests.get")
def test_fetch_top_crypto_assets(mock_get):
    mock_get.return_value.json.return_value = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "image": "https://image.url/bitcoin.png",
            "market_cap_rank": 1
        }
    ]
    mock_get.return_value.raise_for_status = mock.Mock()
    results = services.fetch_top_crypto_assets()
    assert isinstance(results, list)
    assert results[0]["id"] == "bitcoin"

@pytest.mark.django_db
@mock.patch("crypto.services.fetch_top_crypto_assets")
def test_ingest_top_crypto_assets(mock_fetch):
    mock_fetch.return_value = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "image": "https://image.url/bitcoin.png",
            "market_cap_rank": 1,
            "current_price": 29500.0,
            "market_cap": 1000000000,
            "total_volume": 25000000
        }
    ]

    services.ingest_top_crypto_assets()
    asset = CryptoAsset.objects.get(symbol="btc")
    assert asset.name == "Bitcoin"
    assert CryptoPrice.objects.filter(asset=asset).exists()
