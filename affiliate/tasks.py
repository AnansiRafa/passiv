from celery import shared_task
from .models import AffiliateLink

@shared_task
def reset_click_counts():
    AffiliateLink.objects.all().update(click_count=0)
