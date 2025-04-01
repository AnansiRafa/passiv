from .models import AffiliateLink


def track_affiliate_click(link_id):
    """
    Increments the click count for an affiliate link.
    """
    try:
        link = AffiliateLink.objects.get(id=link_id)
        link.click_count += 1
        link.save()
        return link.click_count
    except AffiliateLink.DoesNotExist:
        return None
