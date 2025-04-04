# affiliate/services.py

from .models import AffiliateLink


def create_affiliate_link(url: str, description: str) -> AffiliateLink:
    """Create a new affiliate link."""
    return AffiliateLink.objects.create(url=url, description=description)


def track_click(link_id: int) -> int:
    """Increment and return the click count for an affiliate link."""
    link = AffiliateLink.objects.get(id=link_id)
    link.click_count += 1
    link.save()
    return link.click_count
