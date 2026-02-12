# tests/ui/test_checkout.py
"""Cart and checkout functionality tests."""

import logging

import pytest

from pages.cart_page import CartPage

logger = logging.getLogger(__name__)


class TestCheckout:
    """Verifies cart operations and checkout availability."""

    @pytest.mark.checkout
    @pytest.mark.regression
    def test_cart_has_checkout_button(self, page):
        """CartPage exposes a callable `proceed_to_checkout` method."""
        logger.info("Testing cart checkout button availability...")
        cart_page = CartPage(page)

        assert hasattr(cart_page, "proceed_to_checkout"), (
            "Cart page missing proceed_to_checkout method"
        )
        assert callable(getattr(cart_page, "proceed_to_checkout")), (
            "proceed_to_checkout should be callable"
        )
        logger.info("✓ Cart checkout functionality available")

    @pytest.mark.checkout
    @pytest.mark.regression
    @pytest.mark.parametrize("expected_type", [int])
    def test_cart_item_count_returns_integer(self, page, expected_type):
        """get_cart_items_count() returns an int."""
        logger.info("Testing cart item count returns correct type...")
        cart_page = CartPage(page)

        item_count = cart_page.get_cart_items_count()
        assert isinstance(item_count, expected_type), (
            f"Expected {expected_type}, got {type(item_count)}"
        )
        logger.info(f"✓ Cart item count is valid integer: {item_count}")
