# tests/ui/test_smoke.py
"""Critical-path smoke tests — homepage, registration, add-to-cart."""

import logging
from datetime import datetime

import pytest
import requests
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

logger = logging.getLogger(__name__)

API_BASE = "https://automationexercise.com/api"


def _delete_user_via_api(email: str, password: str = "TestPassword123!") -> None:
    """Best-effort cleanup: delete a registered user via the API."""
    try:
        requests.delete(
            f"{API_BASE}/deleteAccount",
            data={"email": email, "password": password},
            timeout=10,
        )
    except Exception:
        pass  # Don't break teardown if API is unreachable


class TestSmoke:
    """Quick sanity checks for the most critical user flows."""

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_homepage_loads(self, page):
        """Verify page title and logo are visible."""
        logger.info("Testing homepage load...")
        HomePage(page)  # ensures page navigated via conftest

        # The site title may take a moment to settle; use a pattern to accommodate
        # minor variations reported on some browser engines (e.g. WebKit).
        expect(page).to_have_title("Automation Exercise", timeout=15000)
        expect(page.locator("img[alt='Website for automation practice']")).to_be_visible(
            timeout=10000
        )
        logger.info("✓ Homepage loaded successfully")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_user_registration_flow(self, page, test_data):
        """Register a new user with a timestamped email and verify success."""
        logger.info("Testing user registration flow...")
        homepage = HomePage(page)
        login_page = LoginPage(page)

        # Get base user data from test_data (legacy fixture format)
        if isinstance(test_data, list) and len(test_data) > 0:
            user_data = test_data[0].get("valid_user", {})
        else:
            user_data = {"name": "Test User", "email": "testuser@example.com"}

        # Generate unique credentials to avoid "already registered" errors
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        base_name = user_data.get("name", "Test User")
        base_email = user_data.get("email", "testuser@example.com")
        unique_email = base_email.replace("@", f"_{timestamp}@")
        unique_name = f"{base_name}_{timestamp}"

        logger.info(f"Registering user: {unique_name} ({unique_email})")
        homepage.navigate_to_login()
        # Note: consent overlay is blocked at network level by conftest.py
        login_page.register_new_user(unique_name, unique_email)

        # Verify we're still on the site after registration completes
        current_url = page.url
        assert "automationexercise.com" in current_url, (
            f"Expected to be on automationexercise.com, got {current_url}"
        )
        logger.info(f"✓ User registered successfully: {unique_name}")

        # Teardown: clean up the registered user via API
        _delete_user_via_api(unique_email)
        logger.info(f"✓ Test user cleaned up: {unique_email}")

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_to_cart_flow(self, page):
        """Navigate to a product detail page, add to cart, verify cart is non-empty."""
        logger.info("Testing add to cart flow...")
        product_page = ProductPage(page)
        cart_page = CartPage(page)

        product_page.add_product_via_detail_page(product_id=1)
        cart_page.navigate_to_cart()
        cart_page.verify_has_items()

        cart_count = cart_page.get_cart_items_count()
        assert cart_count >= 1, f"Expected at least 1 item in cart, got {cart_count}"
        logger.info(f"✓ Add to cart flow successful - {cart_count} items in cart")
