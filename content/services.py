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
    content: str,
    opportunity: InvestmentOpportunity,
    changes: str = "",
    metrics: dict = None
) -> ContentVersion:
    metrics = metrics or {}

    latest = ContentVersion.objects.filter(opportunity=opportunity).order_by('-timestamp').first()
    version = (latest.version + 1) if latest else 1

    return ContentVersion.objects.create(
        content=content,
        version=version,
        opportunity=opportunity,
        changes=changes,
        metrics=metrics
    )
