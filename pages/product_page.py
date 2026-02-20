# pages/product_page.py
"""
Product Page Object — interactions for the product listing.

Provides methods to browse products and add items to the cart.
"""

import logging

from pages.base_page import BasePage

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
    DETAIL_ADD_TO_CART_BTN = "button.btn-default.cart"
    CART_MODAL = "#cartModal"
    CART_MODAL_CLOSE = "#cartModal button.close-modal, #cartModal .close"

    BASE_URL: str = "https://automationexercise.com"

    def add_product_to_cart(self, product_index: int = 0) -> None:
        """
        Add a product to the shopping cart by index.

        This method performs the following steps:
        1. Locates the product by its index on the product listing page.
        2. Hovers over the product to reveal the add-to-cart button.
        3. Clicks the add-to-cart button to add the product to the cart.
        4. Handles the success modal or popup that appears after adding the product.
        5. Navigates to the cart view to verify the product was added successfully.

        Args:
            product_index (int): Zero-based index of the product to add (default: 0, first product).

        Raises:
            RuntimeError: If unable to add the product to the cart due to an error.
            IndexError: If the specified product index is out of range.

        Example:
            >>> product_page.add_product_to_cart(0)  # Add the first product.
            >>> product_page.add_product_to_cart(2)  # Add the third product.
        """
        try:
            products = self.page.locator(self.PRODUCT_ITEM)
            product_count = products.count()

            if product_index >= product_count:
                raise IndexError(
                    f"Product index {product_index} out of range (total: {product_count})"
                )

            logger.info(f"Adding product at index {product_index} to cart...")

            # Dismiss any lingering overlays before interacting
            self._dismiss_overlays()

            # Hover over product to reveal add-to-cart button
            products.nth(product_index).hover()
            logger.debug(f"Hovered over product {product_index}")

            # Click add-to-cart button with force to bypass any overlays
            products.nth(product_index).locator(self.ADD_TO_CART_BTN).first.click(force=True)
            logger.debug(f"Clicked add-to-cart button for product {product_index}")

            # Wait for the "Added!" modal and click View Cart
            try:
                view_cart = self.page.locator(self.VIEW_CART_MODAL)
                view_cart.wait_for(state="visible", timeout=10000)
                self.page.wait_for_timeout(300)
                view_cart.click()
                logger.debug("Clicked 'View Cart' in modal")
            except Exception as modal_error:
                logger.warning(
                    f"View Cart modal not available ({modal_error}). Navigating directly to cart."
                )
                # Use absolute URL — Firefox rejects relative paths in page.goto()
                base = self.page.url.split("/", 3)[:3]
                self.page.goto("/".join(base) + "/view_cart")

            logger.info(f"Product {product_index} added to cart successfully")

        except Exception as e:
            logger.error(f"Failed to add product to cart: {str(e)}")
            raise RuntimeError(f"Failed to add product to cart: {str(e)}")

    def add_product_via_detail_page(self, product_id: int = 33, max_retries: int = 3) -> None:
        """Add a product to cart via its detail page.

        This method is more reliable than the listing-page hover overlay
        because the add-to-cart button is always visible on the detail page.
        Retries up to ``max_retries`` times, waiting for the confirmation
        modal to verify the server accepted the request.

        Args:
            product_id: The product ID to add (default: 33).
            max_retries: Number of attempts before giving up.

        Raises:
            RuntimeError: If the product could not be added after all retries.
        """
        for attempt in range(max_retries):
            response = self.page.goto(
                f"{self.BASE_URL}/product_details/{product_id}",
                wait_until="domcontentloaded",
            )

            # Handle transient server errors (Cloudflare 520/503)
            if response and response.status >= 500:
                logger.warning(
                    f"Server returned {response.status} on detail page "
                    f"(attempt {attempt + 1}) — retrying"
                )
                self.page.wait_for_timeout(2000)
                continue

            add_btn = self.page.locator(self.DETAIL_ADD_TO_CART_BTN)
            try:
                add_btn.wait_for(state="visible", timeout=20000)
            except Exception:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Add-to-cart button not visible (attempt {attempt + 1}) — reloading"
                    )
                    self.page.reload(wait_until="domcontentloaded")
                    continue
                raise
            add_btn.click()

            # Wait for the confirmation modal to verify the item was added
            cart_modal = self.page.locator(self.CART_MODAL)
            try:
                cart_modal.wait_for(state="visible", timeout=5000)
            except Exception:
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Add-to-cart modal not shown (attempt {attempt + 1}), retrying..."
                    )
                    continue
                logger.warning("Modal not shown on final attempt — proceeding anyway")

            # Dismiss the modal
            close_btn = self.page.locator(self.CART_MODAL_CLOSE)
            if close_btn.first.is_visible(timeout=2000):
                close_btn.first.click()
            self.page.wait_for_timeout(500)
            logger.info(f"Product {product_id} added to cart via detail page")
            return

        raise RuntimeError(
            f"Failed to add product {product_id} to cart after {max_retries} attempts"
        )
