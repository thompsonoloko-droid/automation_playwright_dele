# tests/api/test_product_api.py
"""API tests for product endpoints (API 1, 2, 5 & 6) — data-driven from test_data.json."""

import logging

import pytest
import requests

from tests.api.conftest import BASE_URL, TIMEOUT, _load_api_config

logger = logging.getLogger(__name__)


def _search_terms() -> list[str]:
    """Return search terms for parametrized product search tests."""
    return _load_api_config().get("search_terms", ["Top"])


class TestProductAPI:
    """Data-driven API tests for product listing and search endpoints."""

    @pytest.mark.api
    def test_get_products_list(self):
        """API 1: GET /productsList returns a non-empty products array."""
        logger.info("Testing products list endpoint...")

        response = requests.get(f"{BASE_URL}/productsList", timeout=TIMEOUT)

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
        payload = {"search_product": search_term}

        response = requests.post(f"{BASE_URL}/searchProduct", data=payload, timeout=TIMEOUT)

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()

        assert "products" in data, "Response missing 'products' field"
        assert len(data["products"]) > 0, f"No products found for '{search_term}'"

        for product in data["products"]:
            assert "name" in product, "Product missing 'name' field"
            assert isinstance(product["name"], str), "Product name should be a string"

        logger.info(f"✓ Found {len(data['products'])} products for '{search_term}'")


class TestProductAPIEdgeCases:
    """API tests for product endpoint edge cases and unsupported methods."""

    @pytest.mark.api
    def test_post_to_products_list_returns_405(self):
        """
        API 2: POST /productsList is not supported.

        Verifies the endpoint rejects POST with responseCode 405.
        """
        logger.info("Testing POST to products list (unsupported)...")
        response = requests.post(f"{BASE_URL}/productsList", timeout=TIMEOUT)

        assert response.status_code == 200
        data = response.json()
        assert data["responseCode"] == 405
        assert "not supported" in data.get("message", "").lower()

        logger.info("✓ POST to /productsList correctly rejected with 405")

    @pytest.mark.api
    def test_search_product_without_param(self):
        """
        API 6: POST /searchProduct without search_product parameter.

        Verifies the endpoint returns responseCode 400 when the required
        search parameter is omitted.
        """
        logger.info("Testing search without required parameter...")
        response = requests.post(f"{BASE_URL}/searchProduct", timeout=TIMEOUT)

        assert response.status_code == 200
        data = response.json()
        assert data["responseCode"] == 400, f"Expected 400, got {data['responseCode']}"
        assert "parameter" in data.get("message", "").lower()

        logger.info("✓ Missing search param correctly returns 400")
