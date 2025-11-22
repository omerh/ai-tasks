"""Amazon Product Advertising API integration with OffersV2 support"""

import os
from turtle import resetscreen
from typing import Optional

from loguru import logger
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.models.search_items_resource import SearchItemsResource
from paapi5_python_sdk.rest import ApiException

from src.data.amazon import AmazonItem


def search_items_with_deals(
    keyword: str, min_discount_percentage: int = 0, item_count: int = 10
) -> Optional[list[AmazonItem]]:
    """
    Search for Amazon items with deals using PA-API 5.0

    Args:
        keyword: Search keyword (e.g., "iPhone 16 pro case")
        min_discount_percentage: Minimum discount percentage to filter (default: 20%)
        item_count: Number of items to return (max 10 per request)

    Returns:
        List of AmazonItem objects with deal information, or None if error
    """

    # Get credentials from environment
    access_key = os.getenv("PAAPI_ACCESS_KEY")
    secret_key = os.getenv("PAAPI_SECRET_KEY")
    partner_tag = os.getenv("PAAPI_PARTNER_TAG")

    if not all([access_key, secret_key, partner_tag]):
        logger.error("Missing PA-API credentials in environment variables")
        return None

    # PA-API configuration
    host = "webservices.amazon.com"
    region = "us-east-1"

    # Initialize API client
    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    # Specify resources to retrieve - using OffersV2 for deal information
    search_items_resource = [
        SearchItemsResource.ITEMINFO_TITLE,
        SearchItemsResource.ITEMINFO_FEATURES,
        SearchItemsResource.ITEMINFO_BYLINEINFO,
        SearchItemsResource.OFFERSV2_LISTINGS_PRICE,
        SearchItemsResource.OFFERSV2_LISTINGS_DEALDETAILS,
        SearchItemsResource.OFFERSV2_LISTINGS_AVAILABILITY,
        SearchItemsResource.OFFERSV2_LISTINGS_CONDITION,
        SearchItemsResource.CUSTOMERREVIEWS_COUNT,
        SearchItemsResource.CUSTOMERREVIEWS_STARRATING,
        SearchItemsResource.IMAGES_PRIMARY_LARGE,
    ]

    try:
        # Create search request
        search_items_request = SearchItemsRequest(
            partner_tag=partner_tag,
            partner_type=PartnerType.ASSOCIATES,
            keywords=keyword,
            search_index="All",  # Search across all categories
            item_count=item_count,
            resources=search_items_resource,
        )

        logger.info(f"Searching Amazon for: {keyword}")

        # Send request to PA-API
        response = default_api.search_items(search_items_request)
        logger.debug(f"response: {response}")

        if response is None:
            logger.warning("No response from PA-API")
            return None

        if response.search_result is None or response.search_result.items is None:
            logger.warning("No items found in search results")
            return None

        # Parse results and filter by discount
        items_with_deals = []

        for item in response.search_result.items:
            try:
                amazon_item = _parse_item_to_amazon_item(item, min_discount_percentage)
                if amazon_item:
                    items_with_deals.append(amazon_item)
            except Exception as e:
                logger.warning(f"Error parsing item {item.asin}: {e}")
                continue

        logger.info(
            f"Found {len(items_with_deals)} items with {min_discount_percentage}%+ discount"
        )
        return items_with_deals if items_with_deals else None

    except ApiException as e:
        logger.error(e)
        logger.error(f"PA-API Error - Status: {e.status}")
        logger.error(f"Error body: {e.body}")
        if hasattr(e, "headers") and e.headers and "x-amzn-RequestId" in e.headers:
            logger.error(f"Request ID: {e.headers['x-amzn-RequestId']}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error searching items: {e}")
        return None


def _parse_item_to_amazon_item(
    item, min_discount_percentage: int
) -> Optional[AmazonItem]:
    """
    Parse PA-API item response to AmazonItem model
    Only returns items that meet minimum discount requirement
    """

    # Get basic info
    asin = item.asin
    url = item.detail_page_url

    # Get title
    title = ""
    if item.item_info and item.item_info.title and item.item_info.title.display_value:
        title = item.item_info.title.display_value

    # Get features/description
    description = ""
    if (
        item.item_info
        and item.item_info.features
        and item.item_info.features.display_values
    ):
        description = " | ".join(
            item.item_info.features.display_values[:3]
        )  # First 3 features

    # Get OffersV2 data
    if not item.offers_v2 or not item.offers_v2.listings:
        return None  # No offers available

    # Get the buy box winner (best offer)
    buy_box_offer = None
    for listing in item.offers_v2.listings:
        if listing.is_buy_box_winner:
            buy_box_offer = listing
            break

    if not buy_box_offer:
        buy_box_offer = item.offers_v2.listings[0]  # Fallback to first listing

    # Get price
    price = "N/A"
    if buy_box_offer.price and buy_box_offer.price.display_amount:
        price = buy_box_offer.price.display_amount

    # Get deal details and discount
    discount_percentage = 0
    discount_amount = ""

    if buy_box_offer.price and buy_box_offer.price.savings:
        savings = buy_box_offer.price.savings
        if savings.percentage:
            discount_percentage = savings.percentage
        if savings.display_amount:
            discount_amount = savings.display_amount

    # Filter: only return items meeting minimum discount
    if discount_percentage < min_discount_percentage:
        return None

    # Get reviews
    rating = ""
    review_count = ""
    if item.customer_reviews:
        if item.customer_reviews.star_rating:
            rating = str(item.customer_reviews.star_rating.value)
        if item.customer_reviews.count:
            review_count = str(item.customer_reviews.count)

    # Get review summary (not directly available in PA-API, would need separate scraping)
    review_summary = ""

    return AmazonItem(
        asin=asin,
        name=title,
        description=description,
        url=url,
        price=price,
        discount_amount=f"{discount_percentage}% off ({discount_amount})"
        if discount_amount
        else f"{discount_percentage}% off",
        rating=rating,
        amount_of_reviews=review_count,
        review_summary=review_summary,
    )
