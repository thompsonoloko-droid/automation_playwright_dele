# tests/api/test_product_api.py
"""
API Tests for Product Endpoints

This module contains integration tests for the product-related REST API endpoints.
Tests verify that API endpoints function correctly and return valid responses.

API Endpoints Tested:
- GET /productsList - Retrieve all products
- POST /searchProduct - Search products by term

Example:
    pytest tests/api/test_product_api.py -v
    pytest tests/api/test_product_api.py::TestProductAPI::test_get_products_list -v
"""

import logging

import pytest
import requests
from requests.exceptions import ConnectionError, RequestException, Timeout

logger = logging.getLogger(__name__)


class TestProductAPI:
    """
    API integration tests for product endpoints.

    Tests verify:
    - API connectivity
    - Response format and structure
    - HTTP status codes
    - Response data validation
    """

    # Base URL for all API requests
    BASE_URL = "https://automationexercise.com/api"
    # Request timeout to prevent hanging tests
    TIMEOUT = 10  # seconds

    @pytest.mark.api
    def test_get_products_list(self):
        """
        Test retrieving products list from API endpoint.

        Verifies:
        - HTTP 200 response
        - Response contains 'responseCode': 200
        - Response contains 'products' array
        - Products array is not empty

        This ensures the main product listing API works correctly.

        Raises:
            AssertionError: If any verification fails
            RequestException: If API request fails
        """
        logger.info("Testing products list endpoint...")

        try:
            response = requests.get(
                f"{self.BASE_URL}/productsList", timeout=self.TIMEOUT
            )
            response.raise_for_status()  # Raise exception for HTTP errors

            assert (
                response.status_code == 200
            ), f"Expected 200, got {response.status_code}"
            data = response.json()

            assert "responseCode" in data, "Response missing 'responseCode' field"
            assert (
                data["responseCode"] == 200
            ), f"API response code is {data['responseCode']}, expected 200"
            assert "products" in data, "Response missing 'products' field"
            assert len(data["products"]) > 0, "Products list is empty"

            logger.info(f"✓ Successfully retrieved {len(data['products'])} products")
        except Timeout:
            logger.error("Request timeout")
            raise AssertionError("Products list request timed out")
        except ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise AssertionError(f"Failed to connect to API: {str(e)}")
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    @pytest.mark.api
    def test_search_product(self):
        """
        Test product search functionality via API.

        Verifies:
        - HTTP 200 response
        - Search returns 'products' array
        - Search results are not empty
        - Each product has 'name' field (string type)

        Tests the search endpoint with a known search term.
        Helps ensure search functionality works correctly.

        Raises:
            AssertionError: If any verification fails
            RequestException: If API request fails
        """
        logger.info("Testing product search endpoint...")
        search_term = "Top"
        payload = {"search_product": search_term}

        try:
            response = requests.post(
                f"{self.BASE_URL}/searchProduct", data=payload, timeout=self.TIMEOUT
            )
            response.raise_for_status()

            assert (
                response.status_code == 200
            ), f"Expected 200, got {response.status_code}"
            data = response.json()

            assert "products" in data, "Response missing 'products' field"
            assert (
                len(data["products"]) > 0
            ), f"No products found for search term '{search_term}'"

            # Verify returned products match search criteria
            for product in data["products"]:
                assert "name" in product, "Product missing 'name' field"
                assert isinstance(
                    product["name"], str
                ), "Product name should be a string"

            logger.info(
                f"✓ Successfully found {len(data['products'])} products for '{search_term}'"
            )
        except Timeout:
            logger.error("Request timeout")
            raise AssertionError("Product search request timed out")
        except ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise AssertionError(f"Failed to connect to API: {str(e)}")
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
