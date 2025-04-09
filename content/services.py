from .models import ContentVersion
from investment.models import InvestmentOpportunity
import json
from .gpt import generate_content_for_asset


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
    content_id: str = None,
    changes: str = "",
    metrics: dict = None
) -> ContentVersion:
    metrics = metrics or {}

    if not content_id:
        content_id = f"inv_{opportunity.ticker.upper()}"

    latest = (
        ContentVersion.objects.filter(content_id=content_id)
        .order_by("-version")
        .first()
    )
    version = (latest.version + 1) if latest else 1

    return ContentVersion.objects.create(
        content_id=content_id,
        content=content,
        version=version,
        opportunity=opportunity,
        changes=changes,
        metrics=metrics
    )


def create_gpt_content_version(opportunity: InvestmentOpportunity) -> ContentVersion:
    """
    Generates GPT-powered content, calculates metrics, and stores a new content version.
    """
    content = generate_content_for_asset(opportunity)
    # print(content)
    metrics = calculate_content_metrics(content)
    return save_content_version(content, opportunity, changes="Initial GPT generation", metrics=metrics)
