# investment/services.py

from .models import InvestmentOpportunity


def create_investment_opportunity(
    ticker: str, name: str, description: str
) -> InvestmentOpportunity:
    """Create a new or retrieve an existing InvestmentOpportunity."""
    obj, _ = InvestmentOpportunity.objects.get_or_create(
        ticker=ticker, defaults={"opportunity_name": name, "description": description}
    )
    return obj


def analyze_investment(opportunity: InvestmentOpportunity) -> dict:
    """
    Analyze an investment opportunity.
    This is a placeholder for real analysis logic.
    """
    return {"mock_score": 0.7, "risk": "moderate", "trend": "stable"}
