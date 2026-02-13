# tests/api/test_product_api.py
"""API tests for product endpoints (API 1 & 5) — data-driven from test_data.json."""

import json
import logging
from pathlib import Path

import pytest
import requests

from .api_helpers import get_api_session

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
_DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "test_data.json"


def _load_api_config() -> dict:
    """Load the 'api' section from test_data.json."""
    with open(_DATA_FILE) as f:
        return json.load(f)["api"]


def _search_terms() -> list[str]:
    """Return search terms for parametrized product search tests."""
    return _load_api_config().get("search_terms", ["Top"])


_cfg = _load_api_config()
BASE_URL = _cfg["base_url"]
TIMEOUT = _cfg["timeout"]


class TestProductAPI:
    """Data-driven API tests for product listing and search endpoints."""

    @pytest.mark.api
    def test_get_products_list(self):
        """API 1: GET /productsList returns a non-empty products array."""
        logger.info("Testing products list endpoint...")

        session = get_api_session()
        response = session.get(f"{BASE_URL}/productsList", timeout=TIMEOUT)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert data["responseCode"] == 200, f"API response code: {data['responseCode']}"
        assert "products" in data, "Response missing 'products' field"
        assert len(data["products"]) > 0, "Products list is empty"

        logger.info(f"✓ Retrieved {len(data['products'])} products")

    @pytest.mark.api
    @pytest.mark.parametrize("search_term", _search_terms())
    def test_search_product(self, search_term: str):
        """API 5: POST /searchProduct returns matching products for the given term."""
        logger.info(f"Testing product search for '{search_term}'...")
        session = get_api_session()
        payload = {"search_product": search_term}

        response = session.post(
            f"{BASE_URL}/searchProduct", data=payload, timeout=TIMEOUT
        )

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "products" in data, "Response missing 'products' field"
        assert len(data["products"]) > 0, f"No products found for '{search_term}'"

        for product in data["products"]:
            assert "name" in product, "Product missing 'name' field"
            assert isinstance(product["name"], str), "Product name should be a string"

        logger.info(f"✓ Found {len(data['products'])} products for '{search_term}'")
