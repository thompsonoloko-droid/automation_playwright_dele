# tests/ui/test_smoke.py
"""Critical-path smoke tests — homepage, registration, add-to-cart."""

import logging
from datetime import datetime

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage

logger = logging.getLogger(__name__)


class TestSmoke:
    """Quick sanity checks for the most critical user flows."""

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_homepage_loads(self, page):
        """Verify page title and logo are visible."""
        logger.info("Testing homepage load...")
        HomePage(page)  # ensures page navigated via conftest

        expect(page).to_have_title("Automation Exercise")
        expect(page.locator("img[alt='Website for automation practice']")).to_be_visible()
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

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_to_cart_flow(self, page):
        """Navigate to products, add one to cart, verify cart is non-empty."""
        logger.info("Testing add to cart flow...")
        homepage = HomePage(page)
        product_page = ProductPage(page)
        cart_page = CartPage(page)

        homepage.navigate_to_products()
        page.locator(".product-image-wrapper").first.wait_for(state="visible", timeout=5000)

        product_page.add_product_to_cart(0)

        # Verify at least one item in the cart
        page.locator("#cart_items tbody tr").first.wait_for(state="visible", timeout=3000)
        cart_count = cart_page.get_cart_items_count()
        assert cart_count >= 1, f"Expected at least 1 item in cart, got {cart_count}"
        logger.info(f"✓ Add to cart flow successful - {cart_count} items in cart")
