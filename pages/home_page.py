# pages/home_page.py
"""
Home Page Object — interactions for the main landing page.

Provides navigation to login, products, cart, and contact pages,
plus verification that a user is logged in.
"""

import logging

from playwright.sync_api import expect

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """
    Page Object Model for the Home/Dashboard page.

    Provides methods for:
    - User authentication (login verification)
    - Navigation to different sections (products, cart, contact)
    - Home page status verification

    Attributes:
        SIGNUP_LOGIN_BTN (str): Locator for Sign Up/Login button
        LOGGED_IN_USER (str): Locator for logged-in user display
        PRODUCTS_BTN (str): Locator for Products navigation button
        CART_BTN (str): Locator for Shopping Cart button
        CONTACT_US_BTN (str): Locator for Contact Us button
    """

    # Locators - CSS/XPath selectors for page elements
    SIGNUP_LOGIN_BTN = "a[href='/login']"
    LOGGED_IN_USER = "//a[contains(text(),'Logged in as')]"
    PRODUCTS_BTN = "a[href='/products']"
    CART_BTN = "a[href='/view_cart']"
    CONTACT_US_BTN = "a[href='/contact_us']"

    def navigate_to_login(self) -> None:
        """Click the Sign Up / Login link to open the auth page."""
        self.click(self.SIGNUP_LOGIN_BTN)
        logger.info("Navigated to login page")

    def verify_logged_in(self, username: str) -> None:
        """
        Assert that the page shows 'Logged in as <username>'.

        Args:
            username: The display name expected after login.

        Raises:
            AssertionError: If the logged-in indicator is missing.
        """
        expect(self.page.locator(self.LOGGED_IN_USER)).to_contain_text(username)
        logger.info(f"User '{username}' verified as logged in")

    def navigate_to_products(self) -> None:
        """Open the Products listing page."""
        self.click(self.PRODUCTS_BTN)
        logger.info("Navigated to products page")

    def navigate_to_cart(self) -> None:
        """Open the Shopping Cart page."""
        self.click(self.CART_BTN)
        logger.info("Navigated to cart page")

    def navigate_to_contact_us(self) -> None:
        """Open the Contact Us page."""
        self.click(self.CONTACT_US_BTN)
        logger.info("Navigated to contact us page")
