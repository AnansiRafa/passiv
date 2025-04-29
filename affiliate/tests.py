import pytest
from affiliate.models import AffiliateLink
from content.services import choose_affiliate

@pytest.mark.django_db
def test_choose_affiliate_returns_stock_link():
    AffiliateLink.objects.create(url="https://stocklink.com", description="Best stock picks available.")
    
    affiliate = choose_affiliate(opportunity=True)
    
    assert affiliate is not None
    assert "stock" in affiliate.description.lower()

@pytest.mark.django_db
def test_choose_affiliate_returns_crypto_link():
    AffiliateLink.objects.create(url="https://cryptolink.com", description="Top crypto choices!")
    
    affiliate = choose_affiliate(crypto_asset=True)
    
    assert affiliate is not None
    assert "crypto" in affiliate.description.lower()

@pytest.mark.django_db
def test_choose_affiliate_returns_none_when_no_links():
    affiliate = choose_affiliate(opportunity=True)
    
    assert affiliate is None

@pytest.mark.django_db
def test_choose_affiliate_returns_none_when_no_matching_tag():
    AffiliateLink.objects.create(url="https://unrelated.com", description="Random link not matching anything.")
    
    affiliate = choose_affiliate(crypto_asset=True)
    
    assert affiliate is None
