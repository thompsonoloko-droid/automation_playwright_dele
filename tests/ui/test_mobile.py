# tests/ui/test_mobile.py
"""Mobile device emulation smoke tests.

These tests verify the site works correctly on mobile viewports and touch
interfaces using Playwright's built-in device emulation.

Usage:
    pytest tests/ui/test_mobile.py -v                               # Default: iPhone 13
    pytest tests/ui/test_mobile.py -v --mobile-device "Pixel 7"     # Specific device
    pytest tests/ui/test_mobile.py -v --mobile-device iphone_15     # Shorthand key
"""

import logging

import pytest
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


class TestMobileSmoke:
    """Smoke tests on mobile device emulation — critical flows on small screens."""

    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_homepage_loads_mobile(self, mobile_page: Page) -> None:
        """Verify the homepage loads correctly on a mobile viewport."""
        logger.info("Testing mobile homepage load...")

        expect(mobile_page).to_have_title("Automation Exercise", timeout=15000)

        # The logo should be visible (may be scaled differently on mobile)
        logo = mobile_page.locator("img[alt='Website for automation practice']")
        expect(logo).to_be_visible(timeout=10000)

        # Verify mobile viewport is smaller than desktop (1920)
        viewport = mobile_page.viewport_size
        assert viewport is not None, "Viewport size should be set"
        assert (
            viewport["width"] < 1000
        ), f"Expected mobile viewport width < 1000px, got {viewport['width']}px"
        logger.info(
            f"✓ Mobile homepage loaded — viewport: {viewport['width']}×{viewport['height']}"
        )

    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_navigation_menu_mobile(self, mobile_page: Page) -> None:
        """Verify key navigation links are accessible on mobile."""
        logger.info("Testing mobile navigation...")

        # Core navigation links should exist (may be in a hamburger menu)
        nav_links = {
            "Products": "a[href='/products']",
            "Cart": "a[href='/view_cart']",
            "Login": "a[href='/login']",
        }

        for name, selector in nav_links.items():
            link = mobile_page.locator(selector).first
            # On mobile, links may be in a collapsed menu — just verify they exist in DOM
            assert (
                link.count() > 0 or mobile_page.locator(selector).count() > 0
            ), f"Navigation link '{name}' not found in DOM"
            logger.info(f"  ✓ '{name}' link present")

        logger.info("✓ Mobile navigation links verified")

    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_products_page_mobile(self, mobile_page: Page) -> None:
        """Verify the products page renders on mobile viewport."""
        logger.info("Testing mobile products page...")

        mobile_page.goto(
            "https://automationexercise.com/products",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        # Products should be visible
        products = mobile_page.locator(".product-image-wrapper")
        products.first.wait_for(state="visible", timeout=15000)

        product_count = products.count()
        assert product_count > 0, "Expected at least one product on mobile"
        logger.info(f"✓ Products page loaded on mobile — {product_count} products visible")

    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_login_page_renders_mobile(self, mobile_page: Page) -> None:
        """Verify the login page form elements are visible on mobile."""
        logger.info("Testing mobile login page...")

        mobile_page.locator("a[href='/login']").first.click()
        mobile_page.wait_for_load_state("domcontentloaded")

        # Login form elements should be visible on mobile
        expect(mobile_page.locator("input[data-qa='login-email']")).to_be_visible(timeout=10000)
        expect(mobile_page.locator("input[data-qa='login-password']")).to_be_visible(timeout=10000)
        expect(mobile_page.locator("button[data-qa='login-button']")).to_be_visible(timeout=10000)

        logger.info("✓ Login form renders correctly on mobile")

    @pytest.mark.mobile
    @pytest.mark.regression
    def test_add_to_cart_mobile(self, mobile_page: Page) -> None:
        """Verify add-to-cart works on mobile (no hover overlay)."""
        logger.info("Testing mobile add-to-cart...")

        mobile_page.goto(
            "https://automationexercise.com/products",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        # On mobile, the add-to-cart button may be visible without hover
        # because hover states don't apply on touch devices.
        product = mobile_page.locator(".product-image-wrapper").first
        product.wait_for(state="visible", timeout=15000)
        product.scroll_into_view_if_needed()

        add_btn = product.locator(".add-to-cart").first
        add_btn.click(force=True)

        # Wait briefly for the cart to update, then navigate to cart
        mobile_page.wait_for_timeout(1000)
        mobile_page.goto(
            "https://automationexercise.com/view_cart",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        # Verify cart has at least one item
        cart_row = mobile_page.locator("#cart_items tbody tr")
        expect(cart_row.first).to_be_visible(timeout=15000)

        cart_count = cart_row.count()
        assert cart_count >= 1, f"Expected at least 1 cart item on mobile, got {cart_count}"
        logger.info(f"✓ Add-to-cart works on mobile — {cart_count} item(s) in cart")

    @pytest.mark.mobile
    @pytest.mark.regression
    def test_responsive_layout_mobile(self, mobile_page: Page) -> None:
        """Verify the page adapts to mobile viewport without horizontal overflow."""
        logger.info("Testing mobile responsive layout...")

        viewport = mobile_page.viewport_size
        assert viewport is not None

        # Check that the page body doesn't overflow horizontally
        body_width = mobile_page.evaluate("document.body.scrollWidth")
        assert (
            body_width <= viewport["width"] + 20
        ), f"Page overflows horizontally: body={body_width}px, viewport={viewport['width']}px"

        logger.info(
            f"✓ Responsive layout OK — body: {body_width}px, viewport: {viewport['width']}px"
        )
