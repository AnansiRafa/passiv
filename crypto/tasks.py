from celery import shared_task
from .services import ingest_top_crypto_assets

@shared_task
def fetch_and_store_crypto_data():
    ingest_top_crypto_assets()
