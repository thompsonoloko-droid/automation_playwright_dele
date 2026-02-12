# tests/api/test_brands_api.py
"""API tests for brand endpoints (API 3 & 4) — data-driven from test_data.json."""

import logging

import pytest
import requests

from tests.api.conftest import BASE_URL, TIMEOUT

logger = logging.getLogger(__name__)


class TestBrandsAPI:
    """API tests for brand-related endpoints."""

    @pytest.mark.api
    def test_get_all_brands(self):
        """
        API 3: GET /brandsList returns all brands.

        Verifies:
        - HTTP 200 status
        - responseCode 200 in body
        - 'brands' array is present and non-empty
        - Each brand has 'id' and 'brand' fields
        """
        logger.info("Testing brands list endpoint...")
        response = requests.get(f"{BASE_URL}/brandsList", timeout=TIMEOUT)

        assert response.status_code == 200
        data = response.json()
        assert data["responseCode"] == 200
        assert "brands" in data
        assert len(data["brands"]) > 0, "Brands list is empty"

        for brand in data["brands"]:
            assert "id" in brand, "Brand missing 'id' field"
            assert "brand" in brand, "Brand missing 'brand' field"

        logger.info(f"✓ Retrieved {len(data['brands'])} brands")

    @pytest.mark.api
    def test_put_brands_list_returns_405(self):
        """
        API 4: PUT /brandsList is not supported.

        Verifies:
        - PUT method returns responseCode 405
        - Response message indicates method not supported
        """
        logger.info("Testing PUT to brands list (unsupported method)...")
        response = requests.put(f"{BASE_URL}/brandsList", timeout=TIMEOUT)

        assert response.status_code == 200  # HTTP status is 200
        data = response.json()
        assert data["responseCode"] == 405, f"Expected 405, got {data['responseCode']}"
        assert "not supported" in data.get("message", "").lower()

        logger.info("✓ PUT correctly rejected with 405")
