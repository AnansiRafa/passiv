import json
from .models import ContentVersion
from investment.models import InvestmentOpportunity


def generate_investment_content(opportunity):
    """
    Generates a simple report for an investment opportunity.
    """
    content = f"Investment Report for {opportunity.ticker}:\n"
    content += f"Opportunity: {opportunity.opportunity_name}\n"
    content += f"Details: {opportunity.description}\n"
    if opportunity.data:
        content += "Analysis:\n" + json.dumps(opportunity.data, indent=2)
    return content


def save_content_version(content_id, content, changes="", metrics=None):
    """
    Saves a new version of the content.
    - Increments the version number.
    - Stores any changes and metrics (like readability or SEO scores).
    """
    metrics = metrics or {}
    # Get the most recent version for this content_id
    latest = (
        ContentVersion.objects.filter(content_id=content_id)
        .order_by("-version")
        .first()
    )
    new_version = (latest.version if latest else 0) + 1
    cv = ContentVersion.objects.create(
        content_id=content_id,
        version=new_version,
        content=content,
        changes=changes,
        metrics=metrics,
    )
    return cv
