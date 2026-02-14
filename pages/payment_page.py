# pages/payment_page.py
"""
Payment Page Object — interactions for the payment/card details page.

Provides methods to fill card details, submit payment, and verify
order confirmation.
"""

import logging

from playwright.sync_api import expect

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class PaymentPage(BasePage):
    """Page Object Model for the Payment page.

    Provides methods for:
    - Filling card details (name, number, CVC, expiry)
    - Submitting payment
    - Verifying order confirmation
    - Post-payment continue and logout

    Attributes:
        INPUT_NAME_ON_CARD: Locator for cardholder name input
        INPUT_CARD_NUMBER: Locator for card number input
        INPUT_CVC: Locator for CVC input
        INPUT_EXPIRY_MONTH: Locator for expiry month input
        INPUT_EXPIRY_YEAR: Locator for expiry year input
        BTN_PAY: Locator for the pay button
        ORDER_CONFIRMATION: Locator for the confirmation message container
        LINK_CONTINUE: Locator for the post-payment continue link
        LINK_LOGOUT: Locator for the logout link
    """

    INPUT_NAME_ON_CARD: str = "input[name='name_on_card']"
    INPUT_CARD_NUMBER: str = "input[name='card_number']"
    INPUT_CVC: str = "input[data-qa='cvc']"
    INPUT_EXPIRY_MONTH: str = "input[data-qa='expiry-month']"
    INPUT_EXPIRY_YEAR: str = "input[data-qa='expiry-year']"
    BTN_PAY: str = "button[data-qa='pay-button']"
    ORDER_CONFIRMATION: str = "#form"
    CONFIRMATION_TEXT: str = "Congratulations! Your order has been confirmed!"
    LINK_CONTINUE: str = "a[data-qa='continue-button'], a:has-text('Continue')"
    LINK_LOGOUT: str = "a[href='/logout']"

    BASE_URL: str = "https://automationexercise.com"

    def fill_card_details(self, card: dict) -> None:
        """Fill all card detail fields from a dictionary.

        Args:
            card: Dictionary with keys 'name', 'number', 'cvc', 'month', 'year'.
        """
        logger.info("Filling card details...")
        self.fill(self.INPUT_NAME_ON_CARD, card["name"])
        self.fill(self.INPUT_CARD_NUMBER, card["number"])
        self.fill(self.INPUT_CVC, card["cvc"])
        self.fill(self.INPUT_EXPIRY_MONTH, card["month"])
        self.fill(self.INPUT_EXPIRY_YEAR, card["year"])
        logger.info("Card details filled")

    def pay_and_confirm(self) -> None:
        """Click 'Pay and Confirm Order' and verify the confirmation message."""
        self.click(self.BTN_PAY)
        expect(self.page.locator(self.ORDER_CONFIRMATION)).to_contain_text(self.CONFIRMATION_TEXT)
        logger.info("Payment confirmed — order placed successfully")

    def continue_after_payment(self) -> None:
        """Click 'Continue' after successful payment."""
        self.page.locator(self.LINK_CONTINUE).click()
        self.page.wait_for_load_state("domcontentloaded")
        logger.info("Clicked Continue after payment")

    def logout(self) -> None:
        """Logout after payment, handling WebKit session-drop gracefully.

        After 'Continue', WebKit may drop the session (user is already
        logged out).  This method handles both cases.
        """
        logout_link = self.page.locator(self.LINK_LOGOUT)
        if logout_link.is_visible(timeout=5000):
            logout_link.click()
            self.page.wait_for_load_state("domcontentloaded")
            logger.info("Logged out successfully")
        else:
            logger.info("Session already expired — navigating to login page")
            self.page.goto(
                f"{self.BASE_URL}/login",
                wait_until="domcontentloaded",
            )

    def verify_on_login_page(self) -> None:
        """Verify we landed on the login/signup page after logout."""
        expect(self.page.get_by_role("heading", name="Login to your account")).to_be_visible()
        expect(self.page.get_by_role("heading", name="New User Signup!")).to_be_visible()
        logger.info("Login page verified")
