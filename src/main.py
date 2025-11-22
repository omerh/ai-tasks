import random

from dotenv import load_dotenv
from loguru import logger

from src.keywords import (
    audio_keywords,
    computer_keywords,
    home_kitchen_keywords,
    mobile_keywords,
    peripheral_keywords,
    smart_home_keywords,
)
from src.utils.llm import generate_facebook_post
from src.utils.paapi import search_items_with_deals

load_dotenv()


def main():
    # Combine all keyword lists
    all_keywords = (
        mobile_keywords
        + computer_keywords
        + audio_keywords
        + peripheral_keywords
        + smart_home_keywords
        + home_kitchen_keywords
    )

    # Pick a random keyword
    random_keyword = random.choice(all_keywords)
    logger.info(f"Searching for: {random_keyword}")

    # Search for items with at least 20% discount using PA-API
    items = search_items_with_deals(
        keyword=random_keyword, min_discount_percentage=0, item_count=10
    )

    if not items:
        logger.error("No items found")
        return

    # Pick the first item (or you could randomize)
    selected_item = items[0]
    logger.info(f"Selected item: {selected_item.name}")

    # Format item info for LLM
    item_info = f"""
Product: {selected_item.name}
Description: {selected_item.description}
Price: {selected_item.price}
Discount: {selected_item.discount_amount}
Rating: {selected_item.rating} stars ({selected_item.amount_of_reviews} reviews)
URL: {selected_item.url}
"""

    # Generate Facebook post
    logger.info("Generating Facebook post...")
    facebook_post = generate_facebook_post(item_info)

    print("\n" + "=" * 60)
    print("FACEBOOK POST:")
    print("=" * 60)
    print(facebook_post)
    print("=" * 60)


if __name__ == "__main__":
    main()
