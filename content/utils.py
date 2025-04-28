"""
Utility helpers for Passiv’s content pipeline.
"""
from __future__ import annotations
import logging

from .gpt import chat_completion  # same thin wrapper you’re already using

log = logging.getLogger(__name__)

_DISCLOSURE_BLOCK = (
    "\n—\n"
    "Not financial advice. Past performance ≠ future results.\n"
    "Contains affiliate links; we may earn a commission.\n"
    "Data sources: IEX Cloud (stocks) · CoinGecko (crypto).\n"
)

_HUMOR_PROMPT = """
You are a dry-witted compliance goblin. Respond with ONE short (≤25-word) humorous
line that references {subject}. English only, no profanity, no investment advice.
Return the line and nothing else.
"""


def _humorous_tail(subject: str) -> str:
    """
    Ask GPT for a one-liner. Falls back to canned quip on error or length breach.
    """
    try:
        out = chat_completion(
            prompt=_HUMOR_PROMPT.format(subject=subject), max_tokens=40, temperature=0.7
        ).strip()
        if 0 < len(out.split()) <= 25:
            return out
    except Exception as exc:  # noqa: BLE001
        log.warning("Humor generation failed: %s", exc)

    return "Our lawyer made us write this; your portfolio makes its own decisions."


def inject_disclosures(body: str, subject: str) -> str:  # public API
    """
    Append legal block + witty tail to a generated article body.

    Parameters
    ----------
    body : str
        The article markdown we’ve just created.
    subject : str
        Ticker (e.g., 'AAPL') or crypto symbol (e.g., 'ETH') for humorous context.
    """
    body = body.rstrip()
    tail = _humorous_tail(subject)
    return f"{body}{_DISCLOSURE_BLOCK}{tail}\n"
