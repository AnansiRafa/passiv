from celery import shared_task
from investment.models import InvestmentOpportunity
from .services import generate_content, save_content_version

@shared_task
def generate_content_for_opportunity(opportunity_id):
    try:
        opportunity = InvestmentOpportunity.objects.get(id=opportunity_id)
        content = generate_content(opportunity)
        save_content_version(opportunity=opportunity, content=content)
    except InvestmentOpportunity.DoesNotExist:
        return {"error": "Opportunity not found"}
