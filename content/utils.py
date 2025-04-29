"""
Utility helpers for Passiv’s content pipeline.
"""
from __future__ import annotations
import logging

from .gpt import chat_completion  # Thin wrapper you’re already using

log = logging.getLogger(__name__)

_DISCLOSURE_BLOCK = (
    "\n---\n"
    "*Not financial advice. Past performance ≠ future results. "
    "Contains affiliate links. Data sources: IEX Cloud (stocks) · CoinGecko (crypto).*"
)

_HUMOR_PROMPT = """
You are a dry-witted compliance goblin. Respond with ONE short (≤25-word) humorous
line that references {subject}. English only, no profanity, no investment advice.
Return the line and nothing else.
"""


def generate_humorous_subheading(subject: str) -> str:
    """
    Generate a witty one-liner to act as a mini-subheading inside the article.
    """
    try:
        out = chat_completion(
            prompt=_HUMOR_PROMPT.format(subject=subject),
            max_tokens=40,
            temperature=0.7
        ).strip()
        if 0 < len(out.split()) <= 25:
            return f"***{out}***"  # Markdown emphasized mini-header
    except Exception as exc:  # noqa: BLE001
        log.warning("Humor generation failed: %s", exc)

    return "***Our lawyer made us write this; your portfolio makes its own decisions.***"


def inject_humor_into_body(body: str, subject: str) -> str:
    """
    Inject a witty subheading after the first paragraph of the content body.
    """
    paragraphs = body.strip().split("\n\n")
    humor_line = generate_humorous_subheading(subject)

    if len(paragraphs) > 1:
        paragraphs.insert(1, humor_line)
    else:
        paragraphs.append(humor_line)

    return "\n\n".join(paragraphs)


def inject_disclosures(body: str) -> str:
    """
    Append the legal compliance block to the very end of the content.
    """
    body = body.rstrip()
    if "Not financial advice" in body:
        return body  # Idempotent: don't double-inject.

    return f"{body}{_DISCLOSURE_BLOCK}\n"
