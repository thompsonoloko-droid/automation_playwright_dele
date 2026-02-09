# web_utils.py
"""
Web Automation Utilities Module

This module provides the WebUtils class with a comprehensive set of utility functions
for common web automation operations using Playwright. It includes wrappers for:
- Element interaction (click, fill, get text)
- Screenshot capture
- Wait conditions (visibility, URL changes)
- Element navigation (scroll, go back, refresh)
- Element queries and lists

These utilities are used throughout the automation framework to provide consistent,
reliable web automation operations with built-in error handling and logging.

Example:
    from utils.web_utils import WebUtils

    web_utils = WebUtils(page)
    web_utils.wait_and_click("button.submit")
    web_utils.fill_field("input[name='email']", "test@example.com")
"""

import time
from typing import Optional, List
from playwright.sync_api import Page, Locator
import logging

logger = logging.getLogger(__name__)


class WebUtils:
    """
    Utility class for common web automation operations using Playwright.

    Provides a collection of helper methods for reliable element interactions,
    waits, navigation, and validation. All methods include built-in error handling
    and logging.

    Attributes:
        page (Page): Playwright Page object for browser interactions

    Example:
        >>> utils = WebUtils(page)
        >>> utils.wait_and_click("button.submit")
    """

    def __init__(self, page: Page):
        """
        Initialize WebUtils with a Playwright Page object.

        Args:
            page (Page): The Playwright Page object to interact with
        """
        self.page = page

    def wait_and_click(self, selector: str, timeout: int = 30000) -> None:
        """
        Wait for element visibility and click it.

        Locates element by selector, waits for it to be visible within timeout,
        then clicks it. Includes error handling and logging.

        Args:
            selector (str): CSS selector to locate the element
            timeout (int): Wait timeout in milliseconds (default: 30000ms)

        Raises:
            Exception: If element cannot be clicked

        Example:
            >>> utils.wait_and_click("button.submit")
        """
        try:
            element = self.page.locator(selector).first
            element.wait_for(state="visible", timeout=timeout)
            element.click()
            logger.debug(f"Clicked element: {selector}")
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {e}")
            raise

    def fill_field(self, selector: str, text: str, timeout: int = 30000) -> None:
        """
        Wait for input field and fill it with text.

        Locates input element, waits for visibility, then fills with provided text.
        Includes error handling and logging.

        Args:
            selector (str): CSS selector for input element
            text (str): Text to fill into the field
            timeout (int): Wait timeout in milliseconds (default: 30000ms)

        Raises:
            Exception: If field cannot be filled

        Example:
            >>> utils.fill_field("input[name='email']", "test@example.com")
        """
        try:
            element = self.page.locator(selector).first
            element.wait_for(state="visible", timeout=timeout)
            element.fill(text)
            logger.debug(f"Filled field {selector} with: {text}")
        except Exception as e:
            logger.error(f"Failed to fill field {selector}: {e}")
            raise

    def get_element_text(self, selector: str, timeout: int = 30000) -> str:
        """
        Get text content from an element.

        Waits for element visibility and retrieves its text content.
        Automatically strips whitespace.

        Args:
            selector (str): CSS selector for element
            timeout (int): Wait timeout in milliseconds (default: 30000ms)

        Returns:
            str: Element's text content (empty string if no text)

        Raises:
            Exception: If element cannot be accessed

        Example:
            >>> text = utils.get_element_text("p.error-message")
        """
        try:
            element = self.page.locator(selector).first
            element.wait_for(state="visible", timeout=timeout)
            text = element.text_content()
            return text.strip() if text else ""
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {e}")
            raise

    def take_screenshot(self, name: Optional[str] = None) -> str:
        """
        Capture a screenshot of the current page.

        Takes a screenshot and saves it with optional naming.
        Automatically timestamps all screenshots.

        Args:
            name (Optional[str]): Descriptive name for screenshot.
                                If None, uses timestamp only.

        Returns:
            str: Full path to saved screenshot file

        Example:
            >>> screenshot = utils.take_screenshot("login_success")
        """
        if not name:
            name = f"screenshot_{int(time.time())}"

        screenshot_path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def wait_for_url_contains(self, text: str, timeout: int = 30000) -> None:
        """
        Wait for URL to contain specific text.

        Useful for verifying navigation and URL-based assertions.

        Args:
            text (str): Text that must appear in the URL
            timeout (int): Wait timeout in milliseconds (default: 30000ms)

        Raises:
            Exception: If URL doesn't contain text within timeout

        Example:
            >>> utils.wait_for_url_contains("/dashboard")
        """
        try:
            self.page.wait_for_url(f"**{text}**", timeout=timeout)
        except Exception as e:
            logger.error(f"URL did not contain '{text}' within {timeout}ms: {e}")
            raise

    def scroll_to_element(self, selector: str) -> None:
        """
        Scroll element into view.

        Scrolls the page to make the element visible in the viewport.

        Args:
            selector (str): CSS selector for element to scroll to

        Example:
            >>> utils.scroll_to_element("button.submit")
        """
        element = self.page.locator(selector).first
        element.scroll_into_view_if_needed()

    def get_all_elements(self, selector: str) -> List[Locator]:
        """
        Get all elements matching a selector.

        Retrieves all elements that match the specified selector.

        Args:
            selector (str): CSS selector for elements

        Returns:
            list: List of Locator objects matching selector

        Example:
            >>> items = utils.get_all_elements("li.product-item")
        """
        return self.page.locator(selector).all()

    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if element is visible within timeout.

        Non-blocking check that returns True/False without raising exceptions.
        Useful for conditional logic.

        Args:
            selector (str): CSS selector for element
            timeout (int): Wait timeout in milliseconds (default: 5000ms)

        Returns:
            bool: True if element is visible, False otherwise

        Example:
            >>> if utils.is_element_visible("div.success"):
            ...     print("Operation successful")
        """
        try:
            self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
            return True
        except:
            return False

    def refresh_page(self) -> None:
        """
        Refresh the current page.

        Reloads the page and waits for network idle state.

        Example:
            >>> utils.refresh_page()
        """
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

    def go_back(self) -> None:
        """
        Navigate back in browser history.

        Goes back one page in browser history and waits for
        network idle state before returning.

        Example:
            >>> utils.go_back()
        """
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")
