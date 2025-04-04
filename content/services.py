# content/services.py

from .models import ContentVersion
from investment.models import InvestmentOpportunity
import json


def generate_content(opportunity: InvestmentOpportunity) -> str:
    content = f"""Investment Report
    
Ticker: {opportunity.ticker}
Opportunity: {opportunity.opportunity_name}
Description: {opportunity.description}
    
Analysis:
{json.dumps(opportunity.data, indent=2)}
"""
    return content


def calculate_content_metrics(content: str) -> dict:
    return {
        "readability_score": 75.0,
        "seo_score": 80.0,
        "word_count": len(content.split()),
        "quality_score": 0.85,
    }


def save_content_version(
    content_id: str, content: str, changes: str = "", metrics: dict = None
) -> ContentVersion:
    metrics = metrics or {}
    latest = (
        ContentVersion.objects.filter(content_id=content_id)
        .order_by("-version")
        .first()
    )
    version = (latest.version if latest else 0) + 1

    return ContentVersion.objects.create(
        content_id=content_id,
        version=version,
        content=content,
        changes=changes,
        metrics=metrics,
    )
