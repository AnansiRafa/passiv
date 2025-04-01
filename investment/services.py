from .models import InvestmentOpportunity


def analyze_investment(ticker):
    """
    Retrieves or creates an investment opportunity and attaches
    a mock analysis result to its 'data' field.
    """
    opportunity, created = InvestmentOpportunity.objects.get_or_create(
        ticker=ticker,
        defaults={
            "opportunity_name": f"Opportunity for {ticker}",
            "description": "This is a placeholder for detailed investment analysis.",
            "data": {},
        },
    )

    # Update the 'data' field with a dummy analysis result
    opportunity.data = {"analysis": f"Market analysis data for {ticker}"}
    opportunity.save()
    return opportunity
