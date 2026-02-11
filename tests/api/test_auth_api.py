# tests/api/test_auth_api.py
"""API tests for authentication endpoints (API 2, 6–10) — data-driven from test_data.json."""

import json
import logging
import os
from pathlib import Path

import pytest
import requests

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------
_DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "test_data.json"


def _load_test_data() -> dict:
    """Load the full test data from test_data.json."""
    with open(_DATA_FILE) as f:
        return json.load(f)


def _api_config() -> dict:
    """Return the 'api' section of test data."""
    return _load_test_data()["api"]


def _resolve_env(value: str) -> str:
    """Resolve $ENV_VAR references in strings."""
    if isinstance(value, str) and value.startswith("$"):
        return os.environ.get(value[1:], value)
    return value


def _valid_users() -> list[tuple[str, str, str]]:
    """Return parametrize-ready tuples (id, email, password) for valid users."""
    data = _load_test_data()
    return [
        (
            u["id"],
            os.environ.get("TEST_USER_EMAIL", ""),
            os.environ.get("TEST_USER_PASSWORD", ""),
        )
        for u in data.get("users", [])
        if u.get("valid")
    ]


def _invalid_login_attempts() -> list[tuple[str, str, str, int, str]]:
    """Return parametrize-ready tuples for invalid API login attempts."""
    api = _api_config()
    return [
        (
            a["id"],
            _resolve_env(a["email"]),
            a["password"],
            a["expected_code"],
            a["expected_message"],
        )
        for a in api.get("invalid_login_attempts", [])
    ]


# Shared config
_cfg = _api_config()
BASE_URL = _cfg["base_url"]
TIMEOUT = _cfg["timeout"]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
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


class TestVerifyLoginAPI:
    """Data-driven API tests for the /verifyLogin authentication endpoint."""

    @pytest.mark.api
    @pytest.mark.login
    @pytest.mark.parametrize("user_id,email,password", _valid_users())
    def test_verify_login_valid_credentials(self, user_id, email, password):
        """
        API 7: POST /verifyLogin with valid email and password.

        Parametrized from test_data.json → users (valid=true).
        """
        logger.info(f"Testing login verification for {user_id}: {email}")
        payload = {"email": email, "password": password}
        response = requests.post(
            f"{BASE_URL}/verifyLogin", data=payload, timeout=TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()
        assert (
            data["responseCode"] == 200
        ), f"Expected 200, got {data['responseCode']}: {data.get('message', '')}"

        logger.info(f"✓ Valid credentials verified for {user_id}")

    @pytest.mark.api
    @pytest.mark.login
    def test_verify_login_without_email(self):
        """
        API 8: POST /verifyLogin without email parameter.

        Verifies the endpoint returns responseCode 400 when email is missing.
        """
        logger.info("Testing login without email parameter...")
        payload = {"password": "SomePassword123"}
        response = requests.post(
            f"{BASE_URL}/verifyLogin", data=payload, timeout=TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()
        assert data["responseCode"] == 400, f"Expected 400, got {data['responseCode']}"
        assert "parameter" in data.get("message", "").lower()

        logger.info("✓ Missing email correctly returns 400")

    @pytest.mark.api
    @pytest.mark.login
    def test_delete_verify_login_returns_405(self):
        """
        API 9: DELETE /verifyLogin is not supported.

        Verifies the endpoint rejects DELETE method with responseCode 405.
        """
        logger.info("Testing DELETE to /verifyLogin (unsupported)...")
        response = requests.delete(f"{BASE_URL}/verifyLogin", timeout=TIMEOUT)

        assert response.status_code == 200
        data = response.json()
        assert data["responseCode"] == 405
        assert "not supported" in data.get("message", "").lower()

        logger.info("✓ DELETE correctly rejected with 405")

    @pytest.mark.api
    @pytest.mark.login
    @pytest.mark.parametrize(
        "cred_id,email,password,expected_code,expected_msg", _invalid_login_attempts()
    )
    def test_verify_login_invalid_credentials(
        self, cred_id, email, password, expected_code, expected_msg
    ):
        """
        API 10: POST /verifyLogin with invalid details.

        Parametrized from test_data.json → api.invalid_login_attempts.
        """
        logger.info(f"Testing invalid login [{cred_id}]: {email}")
        payload = {"email": email, "password": password}
        response = requests.post(
            f"{BASE_URL}/verifyLogin", data=payload, timeout=TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()
        assert (
            data["responseCode"] == expected_code
        ), f"Expected {expected_code}, got {data['responseCode']}"
        assert expected_msg.lower() in data.get("message", "").lower()

        logger.info(f"✓ Invalid login [{cred_id}] correctly returns {expected_code}")
