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

import logging
import time
from typing import Optional

from playwright.sync_api import Locator, Page, expect

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

        This method ensures elements are visible before interaction, reducing flaky tests.

        Args:
            selector (str): CSS selector of the element to wait for.
            timeout (Optional[int]): Maximum time to wait for the element to become visible, in milliseconds.

        Returns:
            Locator: Playwright Locator object for the visible element.

        Raises:
            TimeoutError: If the element does not become visible within the specified timeout.

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
        Wait for an element to be visible and click it.

        This method handles overlays that might block the click action by attempting to dismiss them.

        Args:
            selector (str): CSS selector of the element to click.
            timeout (Optional[int]): Maximum time to wait for the element to become visible, in milliseconds.

        Raises:
            AssertionError: If the click action fails after retrying.

        Example:
            >>> page_obj.click("a[href='/login']")
        """

        try:
            self.wait_for_element(selector, timeout).click()
            logger.debug(f"Clicked element '{selector}'")
        except Exception as e:
            logger.warning(
                f"Click failed due to overlay: {e}. Attempting to dismiss overlay."
            )
            try:
                # Attempt to remove overlay
                self.page.evaluate(
                    """
                    const overlay = document.querySelector('[class*="fc-dialog-overlay"]');
                    if (overlay) overlay.remove();
                """
                )
                logger.debug("Overlay dismissed successfully.")
                self.wait_for_element(selector, timeout).click()
            except Exception as retry_error:
                logger.error(
                    f"Failed to click element '{selector}' after dismissing overlay: {retry_error}"
                )
                # Additional retry logic for stubborn overlays
                try:
                    self.page.evaluate(
                        """
                        const allOverlays = document.querySelectorAll('[class*="overlay"]');
                        allOverlays.forEach(overlay => overlay.remove());
                    """
                    )
                    logger.debug("All overlays dismissed successfully.")
                    self.wait_for_element(selector, timeout).click()
                except Exception as final_error:
                    logger.critical(
                        f"Final attempt to click element '{selector}' failed: {final_error}"
                    )
                    raise AssertionError(
                        f"Unable to click element '{selector}' after multiple attempts."
                    )

    def fill(self, selector: str, text: str, timeout: Optional[int] = None):
        """
        Wait for an input element to be visible and fill it with the specified text.

        This method ensures any existing text is cleared before filling the input field.

        Args:
            selector (str): CSS selector of the input element.
            text (str): The text to input into the field.
            timeout (Optional[int]): Maximum time to wait for the element to become visible, in milliseconds.

        Raises:
            AssertionError: If the input field cannot be filled.

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
        Retrieve the visible text content of an element.

        Args:
            selector (str): CSS selector of the element to retrieve text from.
            timeout (Optional[int]): Maximum time to wait for the element to become visible, in milliseconds.

        Returns:
            str: The visible text content of the element, or an empty string if no text is found.

        Raises:
            AssertionError: If the text content cannot be retrieved.

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

        Screenshots are saved with a timestamp in the reports directory, making them useful for debugging.

        Args:
            name (str): A descriptive name for the screenshot (timestamp is appended automatically).

        Returns:
            str: The file path of the saved screenshot.

        Raises:
            Exception: If the screenshot cannot be captured.

        Example:
            >>> screenshot_path = page_obj.take_screenshot("login_error")
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
        Verify that the current page URL contains the specified text.

        This method is useful for validating navigation and ensuring the correct page is loaded.

        Args:
            text (str): The text that should be present in the URL.
            timeout (Optional[int]): Maximum time to wait for the URL to contain the text, in milliseconds.

        Raises:
            AssertionError: If the URL does not contain the specified text within the timeout.

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
