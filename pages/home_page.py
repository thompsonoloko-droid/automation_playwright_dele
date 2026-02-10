# pages/home_page.py
"""
Home Page Object Module

This module contains the HomePage class, which encapsulates all interactions
and elements specific to the application's home page. It provides methods for
navigation, verification, and common home page operations.

Example:
    from pages.home_page import HomePage

    home_page = HomePage(page)
    home_page.navigate_to_login()
    home_page.verify_logged_in("John Doe")
"""

from playwright.sync_api import expect
from pages.base_page import BasePage
import logging

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
        """
        Navigate to the login/signup page.

        Clicks the Sign Up/Login button to navigate to the authentication page.

        Example:
            >>> home_page.navigate_to_login()
        """
        try:
            self.click(self.SIGNUP_LOGIN_BTN)
            logger.info("Navigated to login page")
        except AssertionError as ae:
            logger.error(f"Assertion error during navigation to login: {str(ae)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during navigation to login: {str(e)}")
            raise

    def verify_logged_in(self, username: str) -> None:
        """
        Verify that a user is logged in with the specified username.

        This assertion confirms the user is authenticated and viewing
        the dashboard/home page in logged-in state.

        Args:
            username (str): Username to verify is logged in

        Raises:
            AssertionError: If username is not found in logged-in indicator

        Example:
            >>> home_page.verify_logged_in("john_doe")
        """
        try:
            expect(self.page.locator(self.LOGGED_IN_USER)).to_contain_text(username)
            logger.info(f"User '{username}' verified as logged in")
        except Exception as e:
            logger.error(f"User '{username}' not logged in: {str(e)}")
            raise AssertionError(f"User '{username}' not logged in: {str(e)}")

    def navigate_to_products(self) -> None:
        """
        Navigate to the products listing page.

        Clicks the products button to view all available products.

        Example:
            >>> home_page.navigate_to_products()
        """
        try:
            self.click(self.PRODUCTS_BTN)
            logger.info("Navigated to products page")
        except Exception as e:
            logger.error(f"Failed to navigate to products: {str(e)}")
            raise

    def navigate_to_cart(self) -> None:
        """
        Navigate to the shopping cart page.

        Clicks the cart button to view the shopping cart contents.

        Example:
            >>> home_page.navigate_to_cart()
        """
        try:
            self.click(self.CART_BTN)
            logger.info("Navigated to cart page")
        except Exception as e:
            logger.error(f"Failed to navigate to cart: {str(e)}")
            raise

    def navigate_to_contact_us(self) -> None:
        """
        Navigate to the contact us page.

        Clicks the contact us button to go to the contact form.

        Example:
            >>> home_page.navigate_to_contact_us()
        """
        try:
            self.click(self.CONTACT_US_BTN)
            logger.info("Navigated to contact us page")
        except Exception as e:
            logger.error(f"Failed to navigate to contact us: {str(e)}")
            raise
