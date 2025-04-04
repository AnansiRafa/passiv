from celery import shared_task
from .models import InvestmentOpportunity
from .services import analyze_investment

@shared_task
def analyze_opportunity(opportunity_id):
    try:
        opportunity = InvestmentOpportunity.objects.get(id=opportunity_id)
        return analyze_investment(opportunity)
    except InvestmentOpportunity.DoesNotExist:
        return {"error": "Opportunity not found"}
