from celery import shared_task
from .models import InvestmentOpportunity
from .services import analyze_investment, fetch_and_store_stock_prices

@shared_task
def analyze_opportunity(opportunity_id):
    try:
        opportunity = InvestmentOpportunity.objects.get(id=opportunity_id)
        return analyze_investment(opportunity)
    except InvestmentOpportunity.DoesNotExist:
        return {"error": "Opportunity not found"}

@shared_task
def fetch_stock_price_history(opportunity_id):
    try:
        opportunity = InvestmentOpportunity.objects.get(id=opportunity_id)
        fetch_and_store_stock_prices(opportunity.ticker, opportunity)
    except InvestmentOpportunity.DoesNotExist:
        return f"Opportunity with ID {opportunity_id} does not exist"