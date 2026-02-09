# pages/base_page.py
"""
Base Page Object Module for Playwright-based UI Automation

This module provides the BasePage class which serves as the foundation for all Page Object Models (POM)
in the automation framework. It encapsulates common web interaction patterns and provides a consistent
interface for page actions across all page objects.

Key Responsibilities:
- Element waiting and visibility checks
- User interaction methods (click, fill, get text)
- Screenshot capture
- URL verification
- Error handling and logging

All page objects should inherit from BasePage to benefit from these common utilities.

Example:
    from pages.base_page import BasePage

    class LoginPage(BasePage):
        EMAIL_INPUT = "input[data-qa='email']"

        def enter_email(self, email: str):
            self.fill(self.EMAIL_INPUT, email)
"""

from playwright.sync_api import Page, Locator, expect
from typing import Optional
import time
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all Page Object Models in the automation framework.

    Provides common methods for interacting with web elements using Playwright
    with built-in waiting, error handling, and logging.

    Attributes:
        page (Page): Playwright Page object for browser interactions
        timeout (int): Default timeout in milliseconds for element waits (default: 30000ms)
    """

    def __init__(self, page: Page):
        """
        Initialize BasePage with a Playwright Page object.

        Args:
            page (Page): The Playwright Page object to interact with
        """
        self.page = page
        self.timeout = 30000  # 30 seconds default timeout

    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """
        Wait for an element to become visible and return its locator.

        This method is fundamental to reliable automation as it ensures elements are
        visible before interaction, reducing flaky tests due to timing issues.

        Args:
            selector (str): CSS selector of element to wait for
            timeout (Optional[int]): Wait timeout in milliseconds (defaults to 30000ms)

        Returns:
            Locator: Playwright Locator object for the visible element

        Raises:
            TimeoutError: If element doesn't become visible within timeout

        Example:
            >>> element = page.wait_for_element("button.submit")
            >>> element.click()
        """
        timeout = timeout or self.timeout
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def click(self, selector: str, timeout: Optional[int] = None):
        """
        Wait for element visibility and click it.

        This is the primary method for clicking elements in the framework.
        Combines waiting and clicking in one operation to ensure reliability.

        Args:
            selector (str): CSS selector of element to click
            timeout (Optional[int]): Wait timeout in milliseconds

        Raises:
            AssertionError: If element cannot be clicked (with descriptive error message)

        Example:
            >>> page_obj.click("a[href='/login']")
        """
        try:
            self.wait_for_element(selector, timeout).click()
            logger.debug(f"Clicked element '{selector}'")
        except Exception as e:
            logger.error(f"Failed to click element '{selector}': {str(e)}")
            raise AssertionError(f"Failed to click on element '{selector}': {str(e)}")

    def fill(self, selector: str, text: str, timeout: Optional[int] = None):
        """
        Wait for element visibility and fill it with text.

        Automatically clears any existing text before filling, ensuring clean input.

        Args:
            selector (str): CSS selector of the input element
            text (str): Text to fill into the element
            timeout (Optional[int]): Wait timeout in milliseconds

        Raises:
            AssertionError: If element cannot be filled (with descriptive error message)

        Example:
            >>> page_obj.fill("input[name='email']", "test@example.com")
        """
        try:
            self.wait_for_element(selector, timeout).fill(text)
            logger.debug(f"Filled element '{selector}' with text")
        except Exception as e:
            logger.error(f"Failed to fill element '{selector}': {str(e)}")
            raise AssertionError(f"Failed to fill element '{selector}': {str(e)}")

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content from an element.

        Retrieves visible text content from the element, handling None gracefully
        by returning empty string.

        Args:
            selector (str): CSS selector of element to retrieve text from
            timeout (Optional[int]): Wait timeout in milliseconds

        Returns:
            str: Text content of the element, or empty string if None

        Raises:
            AssertionError: If element text cannot be retrieved

        Example:
            >>> error_msg = page_obj.get_text("p.error")
            >>> assert "Invalid" in error_msg
        """
        try:
            text = self.wait_for_element(selector, timeout).text_content()
            result = text.strip() if text else ""
            logger.debug(f"Retrieved text from '{selector}': {result[:50]}...")
            return result
        except Exception as e:
            logger.error(f"Failed to get text from element '{selector}': {str(e)}")
            raise AssertionError(
                f"Failed to get text from element '{selector}': {str(e)}"
            )

    def take_screenshot(self, name: str) -> str:
        """
        Capture a screenshot of the current page state.

        Screenshots are automatically timestamped and saved to the reports directory.
        Useful for debugging test failures and validating visual state.

        Args:
            name (str): Descriptive name for the screenshot (will be timestamped automatically)

        Returns:
            str: Path to the saved screenshot file

        Example:
            >>> screenshot_path = page_obj.take_screenshot("login_page_error")
        """
        try:
            timestamp = int(time.time())
            screenshot_path = f"./reports/screenshots/{name}_{timestamp}.png"
            self.page.screenshot(path=screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
            raise

    def verify_url_contains(self, text: str, timeout: Optional[int] = None):
        """
        Verify that the current page URL contains specified text.

        Useful for verifying page navigation and URL-based assertions.

        Args:
            text (str): Text that should be present in the URL
            timeout (Optional[int]): Wait timeout in milliseconds

        Raises:
            AssertionError: If URL doesn't contain the specified text

        Example:
            >>> page_obj.verify_url_contains("/dashboard")
        """
        try:
            expect(self.page).to_have_url(
                f".*{text}.*", timeout=timeout or self.timeout
            )
            logger.debug(f"URL verification passed: contains '{text}'")
        except Exception as e:
            logger.error(f"URL verification failed - doesn't contain '{text}'")
            raise AssertionError(f"URL does not contain '{text}': {str(e)}")
