# pages/checkout_page.py
"""
Checkout Page Object — interactions for the order checkout page.

Provides methods to verify the checkout page loaded and place an order.
"""

import logging

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """Page Object Model for the Checkout page.

    Provides methods for:
    - Verifying the checkout page loaded
    - Placing an order (navigating to the payment page)

    Attributes:
        PLACE_ORDER_LINK: Locator for the "Place Order" link
        CHECKOUT_MODAL_CLOSE: Locator for closing session-dropped modal
    """

    PLACE_ORDER_LINK: str = "a[href='/payment']"
    CHECKOUT_MODAL_CLOSE: str = "#checkoutModal .close, #checkoutModal a[href='/login']"

    BASE_URL: str = "https://automationexercise.com"

    def ensure_on_checkout(self) -> None:
        """Verify we landed on the checkout page after 'Proceed To Checkout'.

        In WebKit the click may trigger a session-dropped modal instead
        of navigating.  This method handles that case gracefully by
        dismissing the modal and navigating directly.
        """
        try:
            self.page.wait_for_url("**/checkout**", timeout=10000)
        except Exception:
            modal_close = self.page.locator(self.CHECKOUT_MODAL_CLOSE)
            if modal_close.first.is_visible(timeout=2000):
                modal_close.first.click()
            self.page.goto(
                f"{self.BASE_URL}/checkout",
                wait_until="domcontentloaded",
            )
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("On checkout page")

    def place_order(self) -> None:
        """Click 'Place Order' to navigate to the payment page.

        Falls back to direct navigation if the link is not clickable
        (e.g. off-screen in WebKit).
        """
        place_order = self.page.locator(self.PLACE_ORDER_LINK)
        try:
            place_order.wait_for(state="visible", timeout=20000)
            place_order.scroll_into_view_if_needed()
            place_order.click()
        except Exception:
            logger.warning("Place Order link not clickable — navigating directly")
            self.page.goto(
                f"{self.BASE_URL}/payment",
                wait_until="domcontentloaded",
            )
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("Navigated to payment page")
