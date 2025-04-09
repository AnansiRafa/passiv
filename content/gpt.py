import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_content_for_asset(asset) -> str:
    """
    Uses GPT to generate content for a given investment or crypto asset.
    Returns plain text or HTML-formatted content.
    """
    system_prompt = (
        "You are a helpful financial content writer. Write an engaging, clear summary "
        "of this asset suitable for everyday investors. Include market trends and insights "
        "without making financial recommendations."
    )

    user_prompt = f"Generate an article about the asset:\n\nName: {asset.name}\nSymbol: {asset.symbol}\nType: {asset.source_type}"

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=1024,
    )

    return response['choices'][0]['message']['content'].strip()
