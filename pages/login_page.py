# pages/login_page.py
"""
Login Page Object Module

This module contains the LoginPage class, which encapsulates all interactions
and elements specific to the login and registration pages. It provides methods for
user authentication, signup, and form validation.

Example:
    from pages.login_page import LoginPage

    login_page = LoginPage(page)
    login_page.login("user@example.com", "password123")
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
        Perform user login with email and password.

        Fills in the login credentials and submits the login form.

        Args:
            email (str): User email address
            password (str): User password

        Raises:
            AssertionError: If login form interaction fails

        Example:
            >>> login_page.login("user@example.com", "securePassword123")
        """
        try:
            logger.info(f"Attempting login with email: {email}")
            self.fill(self.EMAIL_INPUT, email)
            self.fill(self.PASSWORD_INPUT, password)
            self.click(self.LOGIN_BTN)
            logger.info(f"Login submitted for: {email}")
        except Exception as e:
            logger.error(f"Login failed for {email}: {str(e)}")
            raise AssertionError(f"Failed to login: {str(e)}")

    def register_new_user(self, name: str, email: str) -> None:
        """
        Register a new user with name and email.

        Fills in the signup form with user details and submits the registration.

        Args:
            name (str): Full name of the new user
            email (str): Email address for the new account

        Raises:
            AssertionError: If registration form interaction fails

        Example:
            >>> login_page.register_new_user("John Doe", "john@example.com")
        """
        try:
            logger.info(f"Attempting to register user: {name} ({email})")
            self.fill(self.SIGNUP_NAME_INPUT, name)
            self.fill(self.SIGNUP_EMAIL_INPUT, email)
            self.click(self.SIGNUP_BTN)
            logger.info(f"Registration submitted for: {name}")
        except Exception as e:
            logger.error(f"Registration failed for {name}: {str(e)}")
            raise AssertionError(f"Failed to register user: {str(e)}")
