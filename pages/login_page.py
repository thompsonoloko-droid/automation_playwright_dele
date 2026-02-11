# pages/login_page.py
"""
Login Page Object — interactions for the login and signup forms.

Provides methods to log in with existing credentials or
register a new user account.
"""

import logging

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """
    Page Object Model for the Login and Registration page.

    Provides methods for:
    - User login with email and password
    - New user registration
    - Form field interactions

    Attributes:
        EMAIL_INPUT (str): Locator for login email input field
        PASSWORD_INPUT (str): Locator for login password input field
        LOGIN_BTN (str): Locator for login submit button
        SIGNUP_NAME_INPUT (str): Locator for signup name input field
        SIGNUP_EMAIL_INPUT (str): Locator for signup email input field
        SIGNUP_BTN (str): Locator for signup submit button
    """

    # Locators for login form elements
    EMAIL_INPUT = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BTN = "button[data-qa='login-button']"

    # Locators for signup form elements
    SIGNUP_NAME_INPUT = "input[data-qa='signup-name']"
    SIGNUP_EMAIL_INPUT = "input[data-qa='signup-email']"
    SIGNUP_BTN = "button[data-qa='signup-button']"

    def login(self, email: str, password: str) -> None:
        """
        Submit the login form with the given credentials.

        Args:
            email: User’s email address.
            password: User’s password.
        """
        logger.info(f"Logging in as: {email}")
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)
        logger.info(f"Login submitted for: {email}")

    def register_new_user(self, name: str, email: str) -> None:
        """
        Submit the signup form with name and email.

        Args:
            name: Full name for the new account.
            email: Email address for the new account.
        """
        logger.info(f"Registering user: {name} ({email})")
        self.fill(self.SIGNUP_NAME_INPUT, name)
        self.fill(self.SIGNUP_EMAIL_INPUT, email)
        self.click(self.SIGNUP_BTN)
        logger.info(f"Registration submitted for: {name}")
