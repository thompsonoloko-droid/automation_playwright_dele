# pages/product_page.py
"""
Product Page Object Module

This module contains the ProductPage class, which encapsulates all interactions
and elements specific to the product listing and detail pages. It provides methods for
product browsing, searching, and adding items to cart.

Example:
    from pages.product_page import ProductPage

    product_page = ProductPage(page)
    product_page.add_product_to_cart(0)
"""

from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class ProductPage(BasePage):
    """
    Page Object Model for the Product Listing page.

    Provides methods for:
    - Product discovery and browsing
    - Adding products to shopping cart
    - Product modal interactions

    Attributes:
        PRODUCT_ITEM (str): Locator for individual product containers
        ADD_TO_CART_BTN (str): Locator for add to cart buttons
        VIEW_CART_MODAL (str): Locator for view cart link in modal
    """

    # Locators for product page elements
    PRODUCT_ITEM = ".product-image-wrapper"
    ADD_TO_CART_BTN = ".add-to-cart"
    VIEW_CART_MODAL = "a[href='/view_cart']:has-text('View Cart')"

    def add_product_to_cart(self, product_index: int = 0) -> None:
        """
        Add a product to the shopping cart by index.

        This method:
        1. Locates the product by index
        2. Hovers over it to make add-to-cart button visible
        3. Clicks the add-to-cart button
        4. Handles the success modal/popup
        5. Navigates to the cart view

        Args:
            product_index (int): Zero-based index of the product to add (default: 0, first product)

        Raises:
            AssertionError: If unable to add product to cart
            IndexError: If product index is out of range

        Example:
            >>> product_page.add_product_to_cart(0)  # Add first product
            >>> product_page.add_product_to_cart(2)  # Add third product
        """
        try:
            products = self.page.locator(self.PRODUCT_ITEM)
            product_count = products.count()

            if product_index >= product_count:
                raise IndexError(
                    f"Product index {product_index} out of range (total: {product_count})"
                )

            logger.info(f"Adding product at index {product_index} to cart...")

            # Hover over product to reveal add-to-cart button
            products.nth(product_index).hover()
            logger.debug(f"Hovered over product {product_index}")

            # Click add-to-cart button with force to bypass any overlays
            products.nth(product_index).locator(self.ADD_TO_CART_BTN).first.click(
                force=True
            )
            logger.debug(f"Clicked add-to-cart button for product {product_index}")

            # Wait for and handle the success modal
            try:
                self.page.wait_for_selector(self.VIEW_CART_MODAL, timeout=15000)
                self.page.wait_for_timeout(500)  # Give modal time to fully render
                logger.debug("Cart modal appeared, clicking view cart...")
                self.click(self.VIEW_CART_MODAL)
            except:
                # If modal doesn't appear with primary selector, try alternatives
                try:
                    self.page.wait_for_selector(
                        "button:has-text('Continue Shopping')", timeout=10000
                    )
                    logger.debug("Continue shopping button found, clicking it...")
                    self.click("button:has-text('Continue Shopping')")
                except:
                    # If neither button works, navigate directly to cart
                    logger.debug("Navigating directly to cart...")
                    self.click("a[href='/view_cart']:has-text('View Cart')")

            logger.info(f"Product {product_index} added to cart successfully")

        except Exception as e:
            logger.error(f"Failed to add product to cart: {str(e)}")
            raise AssertionError(f"Failed to add product to cart: {str(e)}")
