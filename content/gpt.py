import os
import openai
from investment.models import InvestmentOpportunity

openai.api_key = os.getenv("OPENAI_API_KEY")

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

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=1024
    )

    return response["choices"][0]["message"]["content"].strip()
