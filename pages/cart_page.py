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

    def get_cart_items_count(self) -> int:
        """Return the number of product rows in the cart (0 if empty)."""
        count = self.page.locator(self.CART_ITEMS).count()
        logger.info(f"Cart items count: {count}")
        return count

    def proceed_to_checkout(self) -> None:
        """Click the 'Proceed To Checkout' button."""
        logger.info("Proceeding to checkout...")
        self.click(self.PROCEED_TO_CHECKOUT)
        logger.info("Checkout initiated")

    def is_cart_empty(self) -> bool:
        """Return True if the 'Cart is empty' message is visible."""
        return self.page.locator(self.CART_EMPTY_MSG).count() > 0
