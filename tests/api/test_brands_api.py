# tests/api/test_brands_api.py
"""API tests for brand endpoints (API 3 & 4) — data-driven from test_data.json."""

import json
import logging
from pathlib import Path

import pytest

from .api_helpers import get_api_session

logger = logging.getLogger(__name__)

# Load config from test_data.json for consistency with other API test files
_DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "test_data.json"


def _load_api_config() -> dict:
    """Load the 'api' section from test_data.json."""
    with open(_DATA_FILE) as f:
        return json.load(f)["api"]


_cfg = _load_api_config()
BASE_URL = _cfg["base_url"]
TIMEOUT = _cfg["timeout"]


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
        session = get_api_session()
        response = session.get(f"{BASE_URL}/brandsList", timeout=TIMEOUT)

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
        session = get_api_session()
        response = session.put(f"{BASE_URL}/brandsList", timeout=TIMEOUT)

        assert response.status_code == 200  # HTTP status is 200
        data = response.json()
        assert data["responseCode"] == 405, f"Expected 405, got {data['responseCode']}"
        assert "not supported" in data.get("message", "").lower()

        logger.info("✓ PUT correctly rejected with 405")
