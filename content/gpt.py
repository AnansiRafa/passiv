import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from investment.models import InvestmentOpportunity
from crypto.models import CryptoAsset



def chat_completion(
    prompt: str,
    *,
    model: str = "gpt-4o-mini",
    max_tokens: int = 40,
   temperature: float = 0.7,
) -> str:
    """
    Return the assistant’s reply *content* only.  Keeps callers terse.
    """
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()


def generate_headline(markdown_body: str) -> str:
    prompt = (
        "Give me a punchy, click-worthy headline (≤ 8 words, Title Case) "
        "for the following stock/crypto analysis:\n\n"
        f"{markdown_body[:1500]}"  # keep token cost low
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=12,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip().replace('"', "")


def generate_content_for_asset(asset: InvestmentOpportunity) -> str:
    """
    Generate investment content using GPT-4o for the given InvestmentOpportunity.
    Returns plain text content ready for rendering or storing.
    """

    system_prompt = (
        "You are a skilled financial content writer. Write an informative, engaging, "
        "and easy-to-understand investment summary about the following asset. "
        "Use a confident and professional tone suitable for an investing newsletter, "
        "but do not offer specific financial advice or recommendations."
    )

    user_prompt = (
        f"Asset Name: {asset.opportunity_name}\n"
        f"Ticker: {asset.ticker}\n"
        f"Type: {asset.source_type}\n"
        f"Description: {asset.description}\n\n"
    )

    if asset.data:
        user_prompt += f"Additional Data: {asset.data}\n"

    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.7,
    max_tokens=1024)

    return response.choices[0].message.content.strip()


def generate_content_for_crypto_asset(asset: CryptoAsset) -> str:
    """
    Generate investment content using GPT-4o for a given CryptoAsset.
    Returns plain text content ready for rendering or storing.
    """

    system_prompt = (
        "You are a skilled crypto analyst and financial writer. "
        "Write a high-quality investment summary for the following cryptocurrency. "
        "Include its utility, market rank, and broader significance. "
        "Avoid offering financial advice."
    )

    user_prompt = (
        f"Crypto Name: {asset.name}\n"
        f"Symbol: {asset.symbol}\n"
        f"Coingecko ID: {asset.coingecko_id}\n"
    )

    if asset.market_cap_rank is not None:
        user_prompt += f"Market Cap Rank: {asset.market_cap_rank}\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1024
    )

    return response.choices[0].message.content.strip()