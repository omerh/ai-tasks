from google import genai
from google.genai import types


def generate_facebook_post(item_info: str) -> str:
    client = genai.Client()
    model = "gemini-2.5-flash"
    prompt = f"""
You are a Facebook page post generator expert. You are familiar with Amazon Affiliate rules and best practices, and Facebook page post best practices.
Generate a Facebook page post that will be viral, and engaging, following Amazon Affiliate rules, should be short, precise and engaging
Add all the following hash tags in one line at the end of the post
#Amazon #onlineshop #onlineshopping #sale #ad #affiliatemarketing #discounts #amazonfinds

If there are more appropriate hashtags to add that can increase reach, add them.

This is the context to create the ad from:

{item_info}

"""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="text/plain", temperature=0.2
        ),
    )
    if response.text:
        return response.text
    else:
        return "No result found"
