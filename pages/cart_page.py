# pages/cart_page.py
"""
Cart Page Object — interactions for the shopping cart.

Provides methods to count cart items, proceed to checkout,
and check if the cart is empty.
"""

import logging

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """
    Page Object Model for the Shopping Cart page.

    Provides methods for:
    - Retrieving cart item count
    - Proceeding to checkout
    - Verifying cart status (empty/full)
    - Cart item management

    Attributes:
        CART_ITEMS (str): Locator for cart items table rows
        PROCEED_TO_CHECKOUT (str): Locator for checkout button
        CART_EMPTY_MSG (str): Locator for empty cart message
    """

    # Locators for cart page elements
    CART_ITEMS = "#cart_items tbody tr"
    PROCEED_TO_CHECKOUT = ".check_out"
    CART_EMPTY_MSG = "//p[contains(text(),'Cart is empty')]"

    BASE_URL: str = "https://automationexercise.com"

    def get_cart_items_count(self) -> int:
        """Return the number of product rows in the cart (0 if empty)."""
        count: int = self.page.locator(self.CART_ITEMS).count()
        logger.info(f"Cart items count: {count}")
        return count

    def proceed_to_checkout(self) -> None:
        """Click the 'Proceed To Checkout' button."""
        logger.info("Proceeding to checkout...")
        self.click(self.PROCEED_TO_CHECKOUT)
        logger.info("Checkout initiated")

    def is_cart_empty(self) -> bool:
        """Return True if the 'Cart is empty' message is visible."""
        empty: bool = self.page.locator(self.CART_EMPTY_MSG).count() > 0
        return empty

    def navigate_to_cart(self) -> None:
        """Navigate directly to the cart page."""
        self.page.goto(
            f"{self.BASE_URL}/view_cart",
            wait_until="domcontentloaded",
        )
        logger.info("Navigated to cart page")

    def verify_has_items(self, timeout: int = 15000) -> None:
        """Verify the cart contains at least one product row.

        If items are not visible on the first attempt, reloads the page
        once and retries — works around a Firefox timing issue where
        the cart page loads before the server has committed the item.

        Args:
            timeout: Max time to wait for cart items to appear.

        Raises:
            AssertionError: If no cart items are visible after retry.
        """
        from playwright.sync_api import expect

        cart_row = self.page.locator(self.CART_ITEMS).first
        try:
            expect(cart_row).to_be_visible(timeout=timeout)
        except (AssertionError, Exception):
            logger.warning("Cart items not visible — reloading page and retrying")
            self.page.reload(wait_until="domcontentloaded")
            expect(cart_row).to_be_visible(timeout=timeout)

        logger.info(f"Cart verified — {self.get_cart_items_count()} item(s)")
