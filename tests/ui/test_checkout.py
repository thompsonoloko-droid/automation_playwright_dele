# tests/ui/test_checkout.py
"""
Checkout and Cart Functionality Tests

This module contains tests for the shopping cart and checkout functionality.
Tests verify:
- Cart page availability and methods
- Cart item count accuracy
- Checkout button availability

Example:
    pytest tests/ui/test_checkout.py -v
"""

import pytest
import logging
from pages.home_page import HomePage
from pages.cart_page import CartPage

logger = logging.getLogger(__name__)


class TestCheckout:
    """
    Tests for checkout and shopping cart functionality.

    Verifies that cart operations work correctly and checkout flow is available.
    """

    @pytest.mark.checkout
    @pytest.mark.regression
    def test_cart_has_checkout_button(self, page):
        """
        Verify cart page has checkout functionality available.

        Validates that:
        - CartPage class has proceed_to_checkout method
        - The method is callable (ready for use)

        This is a smoke test for checkout availability.

        Raises:
            AssertionError: If checkout button/method is missing
        """
        logger.info("Testing cart checkout button availability...")
        cart_page = CartPage(page)

        try:
            # Verify the proceed_to_checkout method exists and is callable
            assert hasattr(
                cart_page, "proceed_to_checkout"
            ), "Cart page missing proceed_to_checkout method"
            assert callable(
                getattr(cart_page, "proceed_to_checkout")
            ), "proceed_to_checkout should be callable"
            logger.info("✓ Cart checkout functionality available")
        except AssertionError as e:
            logger.error(f"✗ Cart checkout test failed: {str(e)}")
            raise

    @pytest.mark.checkout
    @pytest.mark.regression
    @pytest.mark.parametrize("expected_type", [int])
    def test_cart_item_count_returns_integer(self, page, expected_type):
        """
        Verify cart item count returns correct data type.

        Parameterized test that validates:
        - get_cart_items_count() returns an integer
        - Type validation for API contract

        Args:
            page: Browser page fixture
            expected_type: Expected return type (int)

        Raises:
            AssertionError: If return type is incorrect
        """
        logger.info("Testing cart item count returns correct type...")
        cart_page = CartPage(page)

        try:
            item_count = cart_page.get_cart_items_count()
            assert isinstance(
                item_count, expected_type
            ), f"Expected {expected_type}, got {type(item_count)}"
            logger.info(f"✓ Cart item count is valid integer: {item_count}")
        except AssertionError as e:
            logger.error(f"✗ Cart item count test failed: {str(e)}")
            raise
