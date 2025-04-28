from .models import ContentVersion
from investment.models import InvestmentOpportunity
from affiliate.models import AffiliateLink
from crypto.models import CryptoAsset
import json
from .gpt import generate_content_for_asset, generate_content_for_crypto_asset, generate_headline
from textblob import TextBlob
import re
import random
from typing import Optional

from .gpt import (
    generate_content_for_asset,
    generate_content_for_crypto_asset,
)
from .utils import inject_disclosures


def choose_affiliate(opportunity=None, crypto_asset=None) -> Optional["AffiliateLink"]:
    """Return a link whose description contains 'stock' or 'crypto'."""
    tag = "crypto" if crypto_asset else "stock"
    links = AffiliateLink.objects.filter(description__icontains=tag)
    return random.choice(links) if links.exists() else None


def generate_content(opportunity: InvestmentOpportunity) -> str:
    content = f"""Investment Report

Ticker: {opportunity.ticker}
Opportunity: {opportunity.opportunity_name}
Description: {opportunity.description}

Analysis:
{json.dumps(opportunity.data, indent=2)}
"""
    return content


def calculate_content_metrics(text: str) -> dict:
    """
    Given a string of content, return a dictionary of content metrics.
    """
    word_count = len(text.split())

    # Sentence count via basic punctuation split
    sentences = re.split(r'[.!?]', text)
    sentence_count = len([s for s in sentences if s.strip()]) or 1

    # Syllables: rough estimation
    syllable_count = sum(len(re.findall(r'[aeiouy]+', word.lower())) for word in text.split())

    # Flesch Reading Ease Score
    readability_score = 206.835 - (1.015 * (word_count / sentence_count)) - (84.6 * (syllable_count / word_count))

    # Sentiment (range: -1 to 1)
    sentiment = TextBlob(text).sentiment.polarity

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "readability_score": round(readability_score, 2),
        "sentiment": round(sentiment, 3)
    }


def save_content_version(
    content: str,
    opportunity: InvestmentOpportunity = None,
    crypto_asset: CryptoAsset = None,
    content_id: str = None,
    changes: str = "",
    metrics: dict = None,
    title: str = "",
) -> ContentVersion:
    metrics = metrics or {}

    link = choose_affiliate(opportunity, crypto_asset)
    if link:
        content += (
            f"\n\n[Partner link]({link.url}) _(affiliate)_\n"
            "_Disclosure: we may earn a commission; not financial advice._"
        )

    if not content_id:
        if opportunity:
            content_id = f"inv_{opportunity.ticker.upper()}"
        elif crypto_asset:
            content_id = f"crypto_{crypto_asset.symbol.upper()}"
        else:
            raise ValueError("Either opportunity or crypto_asset must be provided.")

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
        crypto_asset=crypto_asset,
        changes=changes,
        metrics=metrics,
        title=title,
    )



def create_gpt_content_version(opportunity: InvestmentOpportunity) -> ContentVersion:
    """
    Generates GPT-powered content, calculates metrics, and stores a new content version.
    """
    content = generate_content_for_asset(opportunity)
    # print(content)
    metrics = calculate_content_metrics(content)
    headline = generate_headline(content)
    return save_content_version(
        content, 
        opportunity, 
        changes="Initial GPT generation", 
        metrics=metrics, 
        title=headline,
    )


def create_gpt_content_version_for_crypto(asset: CryptoAsset) -> ContentVersion:
    """
    Generate and store GPT-powered content for a CryptoAsset.
    """
    content = generate_content_for_crypto_asset(asset)
    metrics = calculate_content_metrics(content)
    headline = generate_headline(content)

    return save_content_version(
        content=content,
        opportunity=None,
        crypto_asset=asset,
        content_id=f"crypto_{asset.symbol.upper()}",
        changes="Initial GPT crypto generation",
        metrics=metrics,
        title=headline,
    )