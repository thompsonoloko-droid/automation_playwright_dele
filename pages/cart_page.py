# pages/cart_page.py
"""
Cart Page Object Module

This module contains the CartPage class, which encapsulates all interactions
and elements specific to the shopping cart page. It provides methods for
managing cart items, checkout, and cart status verification.

Example:
    from pages.cart_page import CartPage

    cart_page = CartPage(page)
    item_count = cart_page.get_cart_items_count()
    cart_page.proceed_to_checkout()
"""

from pages.base_page import BasePage
import logging

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
        """
        Get the total number of items currently in the cart.

        Counts the number of product rows in the cart items table.

        Returns:
            int: Number of items in cart (0 if empty)

        Raises:
            AssertionError: If unable to count cart items

        Example:
            >>> count = cart_page.get_cart_items_count()
            >>> assert count == 3
        """
        try:
            count = self.page.locator(self.CART_ITEMS).count()
            logger.info(f"Cart items count: {count}")
            return count
        except Exception as e:
            logger.error(f"Failed to get cart items count: {str(e)}")
            raise AssertionError(f"Failed to get cart items count: {str(e)}")

    def proceed_to_checkout(self) -> None:
        """
        Click the proceed to checkout button.

        Initiates the checkout process and navigates to the checkout page.

        Raises:
            AssertionError: If unable to proceed to checkout

        Example:
            >>> cart_page.proceed_to_checkout()
        """
        try:
            logger.info("Proceeding to checkout...")
            self.click(self.PROCEED_TO_CHECKOUT)
            logger.info("Checkout initiated successfully")
        except Exception as e:
            logger.error(f"Failed to proceed to checkout: {str(e)}")
            raise AssertionError(f"Failed to proceed to checkout: {str(e)}")

    def is_cart_empty(self) -> bool:
        """
        Check if the shopping cart is empty.

        Verifies if the empty cart message is displayed.

        Returns:
            bool: True if cart is empty, False otherwise

        Example:
            >>> if cart_page.is_cart_empty():
            ...     print("Add items to continue shopping")
        """
        try:
            is_empty = self.page.locator(self.CART_EMPTY_MSG).count() > 0
            logger.debug(f"Cart empty status: {is_empty}")
            return is_empty
        except Exception as e:
            logger.error(f"Failed to check cart empty status: {str(e)}")
            return False
