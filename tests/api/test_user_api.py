# tests/api/test_user_api.py
"""API tests for user account CRUD (API 11–14) — data-driven from test_data.json."""

import logging
import uuid

import pytest
import requests

from tests.api.conftest import BASE_URL, TIMEOUT, _load_api_config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
_cfg = _load_api_config()
_USER_TEMPLATE = _cfg["test_user_template"]
_UPDATE_TEMPLATE = _cfg["update_user_template"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _unique_email() -> str:
    """Generate a unique test email using UUID to avoid collisions in parallel runs."""
    return f"testbot_{uuid.uuid4().hex[:12]}@example.com"


def _create_test_user(email: str, password: str | None = None) -> dict:
    """Register a user using the template from test data and return the response."""
    password = password or _USER_TEMPLATE["password"]
    payload = {**_USER_TEMPLATE, "email": email, "password": password}
    response = requests.post(f"{BASE_URL}/createAccount", data=payload, timeout=TIMEOUT)
    return response.json()


def _delete_test_user(email: str, password: str | None = None) -> dict:
    """Delete a user account."""
    password = password or _USER_TEMPLATE["password"]
    payload = {"email": email, "password": password}
    response = requests.delete(f"{BASE_URL}/deleteAccount", data=payload, timeout=TIMEOUT)
    return response.json()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
class TestUserAccountAPI:
    """Data-driven API tests for user account CRUD operations."""

    @pytest.mark.api
    def test_create_user_account(self):
        """
        API 11: POST /createAccount to register a new user.

        Uses test_user_template from test_data.json for registration fields.
        """
        email = _unique_email()
        logger.info(f"Creating test user: {email}")
        try:
            data = _create_test_user(email)
            logger.info(f"Create user response: {data}")
            assert data.get("responseCode") == 201, (
                f"Expected 201, got {data.get('responseCode')}: {data.get('message', '')} | Full response: {data}"
            )
            logger.info("✓ User account created successfully")
        finally:
            cleanup = _delete_test_user(email)
            logger.info(f"✓ Test user cleaned up, delete response: {cleanup}")

    @pytest.mark.api
    def test_delete_user_account(self):
        """
        API 12: DELETE /deleteAccount to remove a user.

        Creates a user first, then verifies deletion returns responseCode 200.
        """
        email = _unique_email()
        create_resp = _create_test_user(email)
        logger.info(f"Create user response: {create_resp}")
        logger.info(f"Deleting test user: {email}")
        data = _delete_test_user(email)
        logger.info(f"Delete user response: {data}")
        assert data.get("responseCode") == 200, (
            f"Expected 200, got {data.get('responseCode')}: {data.get('message', '')} | Full response: {data}"
        )
        logger.info("✓ User account deleted successfully")

    @pytest.mark.api
    def test_update_user_account(self):
        """
        API 13: PUT /updateAccount to modify user details.

        Uses update_user_template from test_data.json for the updated fields.
        """
        email = _unique_email()
        password = _USER_TEMPLATE["password"]
        try:
            create_resp = _create_test_user(email, password)
            logger.info(f"Create user response: {create_resp}")
            logger.info(f"Updating test user: {email}")
            update_payload = {
                **_UPDATE_TEMPLATE,
                "email": email,
                "password": password,
            }
            response = requests.put(
                f"{BASE_URL}/updateAccount", data=update_payload, timeout=TIMEOUT
            )
            data = response.json()
            logger.info(f"Update user response: {data}")
            assert data.get("responseCode") == 200, (
                f"Expected 200, got {data.get('responseCode')}: {data.get('message', '')} | Full response: {data}"
            )
            logger.info("✓ User account updated successfully")
        finally:
            cleanup = _delete_test_user(email, password)
            logger.info(f"✓ Test user cleaned up, delete response: {cleanup}")

    @pytest.mark.api
    def test_get_user_detail_by_email(self):
        """
        API 14: GET /getUserDetailByEmail with email parameter.

        Creates a user, fetches details, verifies expected fields, then cleans up.
        """
        email = _unique_email()
        password = _USER_TEMPLATE["password"]
        try:
            create_resp = _create_test_user(email, password)
            logger.info(f"Create user response: {create_resp}")
            logger.info(f"Fetching user details for: {email}")
            response = requests.get(
                f"{BASE_URL}/getUserDetailByEmail",
                params={"email": email},
                timeout=TIMEOUT,
            )
            data = response.json()
            logger.info(f"Get user detail response: {data}")
            assert data.get("responseCode") == 200, (
                f"Expected 200, got {data.get('responseCode')}: {data.get('message', '')} | Full response: {data}"
            )
            assert "user" in data, "Response missing 'user' field"
            user = data["user"]
            assert user["email"] == email, f"Expected {email}, got {user['email']}"
            for field in ["id", "name", "email", "title", "first_name", "last_name"]:
                assert field in user, f"User object missing '{field}' field"
            logger.info(f"✓ User details retrieved: {user.get('name', user.get('email'))}")
        finally:
            cleanup = _delete_test_user(email, password)
            logger.info(f"✓ Test user cleaned up, delete response: {cleanup}")

    @pytest.mark.api
    def test_get_user_detail_nonexistent_email(self):
        """
        Negative test: GET /getUserDetailByEmail with non-existent email.

        Verifies responseCode 404 for unknown email.
        """
        logger.info("Testing user detail lookup for non-existent email...")
        response = requests.get(
            f"{BASE_URL}/getUserDetailByEmail",
            params={"email": "absolutely_nobody@nope.com"},
            timeout=TIMEOUT,
        )
        data = response.json()
        assert data["responseCode"] == 404, f"Expected 404, got {data['responseCode']}"

        logger.info("✓ Non-existent email correctly returns 404")
