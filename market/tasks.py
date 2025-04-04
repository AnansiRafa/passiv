from celery import shared_task
from .services import record_market_status

@shared_task
def fetch_market_status():
    record_market_status()
