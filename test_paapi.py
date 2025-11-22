#!/usr/bin/env python
"""Quick test to verify paapi5-python-sdk is installed correctly"""

try:
    import paapi5_python_sdk

    print("✓ paapi5_python_sdk imported successfully")

    from paapi5_python_sdk.api.default_api import DefaultApi

    print("✓ DefaultApi imported successfully")

    from paapi5_python_sdk.models.search_items_request import SearchItemsRequest

    print("✓ SearchItemsRequest imported successfully")

    from paapi5_python_sdk.models.search_items_resource import SearchItemsResource

    print("✓ SearchItemsResource imported successfully")

    print("\n✅ All imports successful! SDK is ready to use.")

except ImportError as e:
    print(f"❌ Import failed: {e}")
    exit(1)
