"""Test PA-API access with minimal request"""

import os

from dotenv import load_dotenv
from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.get_items_request import GetItemsRequest
from paapi5_python_sdk.models.get_items_resource import GetItemsResource
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.rest import ApiException

load_dotenv()

access_key = os.getenv("PAAPI_ACCESS_KEY", None)
secret_key = os.getenv("PAAPI_SECRET_KEY", None)
partner_tag = os.getenv("PAAPI_PARTNER_TAG", None)

if partner_tag is None:
    raise ValueError("PAAPI_PARTNER_TAG is not set")

if access_key is None:
    raise ValueError("PAAPI_ACCESS_KEY is not set")

if secret_key is None:
    raise ValueError("PAAPI_SECRET_KEY is not set")

print("Testing with:")
print(f"Access Key: {access_key}")
print(f"Partner Tag: {partner_tag}")
if secret_key is not None:
    print(f"Secret Key: {secret_key[:10]}...")
else:
    print("⚠️ Secret Key not set")

# Try different hosts
hosts = [
    ("webservices.amazon.com", "us-east-1"),
]

for host, region in hosts:
    print(f"\n\nTesting {host} ({region})...")
    default_api = DefaultApi(
        access_key=access_key, secret_key=secret_key, host=host, region=region
    )

    # Simple GetItems request with a known ASIN
    try:
        get_items_request = GetItemsRequest(
            partner_tag=partner_tag,
            partner_type=PartnerType.ASSOCIATES,
            item_ids=["B08N5WRWNW"],  # Example: Amazon Echo Dot
            resources=[GetItemsResource.ITEMINFO_TITLE],
        )

        response = default_api.get_items(get_items_request)

        if response and response.items_result:
            print(f"✅ SUCCESS! API is working for {host}")
            print(
                f"Found item: {response.items_result.items[0].item_info.title.display_value}"
            )
        else:
            print("⚠️ Response but no items")

    except ApiException as e:
        print(f"❌ API Error: Status {e.status}")
        print(f"Body: {e.body}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
