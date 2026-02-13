# tests/api/test_auth_api.py
"""API tests for authentication endpoints (API 7–10) — data-driven from test_data.json."""

import logging
import os

import pytest
import requests

from tests.api.conftest import BASE_URL, TIMEOUT, _load_api_config, _load_test_data, _resolve_env

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------


def _valid_users() -> list[tuple[str, str, str]]:
    """Return parametrize-ready tuples (id, email, password) for valid users.

    Reads credentials from TEST_USER_EMAIL / TEST_USER_PASSWORD env vars.
    Returns an empty list when the env vars are missing so the test is
    automatically skipped (no parametrize args → collected 0 items).
    """
    email = os.environ.get("TEST_USER_EMAIL", "")
    password = os.environ.get("TEST_USER_PASSWORD", "")
    if not email or not password:
        return []
    data = _load_test_data()
    return [(u["id"], email, password) for u in data.get("users", []) if u.get("valid")]


def _invalid_login_attempts() -> list[tuple[str, str, str, int, str]]:
    """Return parametrize-ready tuples for invalid API login attempts."""
    api = _load_api_config()
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


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
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
        response = requests.post(f"{BASE_URL}/verifyLogin", data=payload, timeout=TIMEOUT)

        assert response.status_code == 200
        data = response.json()
        assert data["responseCode"] == 200, (
            f"Expected 200, got {data['responseCode']}: {data.get('message', '')}"
        )

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
        response = requests.post(f"{BASE_URL}/verifyLogin", data=payload, timeout=TIMEOUT)

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
        response = requests.post(f"{BASE_URL}/verifyLogin", data=payload, timeout=TIMEOUT)

        assert response.status_code == 200
        data = response.json()
        assert data["responseCode"] == expected_code, (
            f"Expected {expected_code}, got {data['responseCode']}"
        )
        assert expected_msg.lower() in data.get("message", "").lower()

        logger.info(f"✓ Invalid login [{cred_id}] correctly returns {expected_code}")
