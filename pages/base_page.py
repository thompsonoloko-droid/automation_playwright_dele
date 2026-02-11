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

    def click(
        self,
        selector: str,
        timeout: Optional[int] = None,
        max_retries: int = 5,
        retry_delay: float = 1.0,
    ):
        """
        Wait for an element to be visible and click it, with robust overlay and popup handling.

        Args:
            selector (str): CSS selector of the element to click.
            timeout (Optional[int]): Maximum time to wait for the element to become visible, in milliseconds.
            max_retries (int): Number of retry attempts if click fails due to overlays.
            retry_delay (float): Delay in seconds between retries.

        Raises:
            AssertionError: If the click action fails after all retries.

        Example:
            >>> page_obj.click("a[href='/login']")
        """
        import time

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                self.wait_for_element(selector, timeout).click()
                logger.debug(f"Clicked element '{selector}' on attempt {attempt}")
                return
            except Exception as e:
                last_error = e
                logger.warning(f"Click attempt {attempt} failed for '{selector}': {e}")
                # Try to dismiss overlays/popups/consent dialogs
                try:
                    # Remove known overlays
                    self.page.evaluate(
                        """
                        const overlays = document.querySelectorAll('[class*="overlay"], [class*="fc-dialog-overlay"], .modal, .popup, .backdrop');
                        overlays.forEach(overlay => overlay.remove());
                    """
                    )
                    # Try to click common consent/close buttons
                    for btn_selector in [
                        "button[aria-label='Close']",
                        "button[aria-label='Dismiss']",
                        "button[aria-label='Consent']",
                        "button:has-text('Close')",
                        "button:has-text('Dismiss')",
                        "button:has-text('Consent')",
                        ".close-button",
                        ".cookie-consent-accept",
                    ]:
                        btns = self.page.locator(btn_selector)
                        if btns.count() > 0:
                            try:
                                btns.first.click(timeout=2000)
                                logger.info(
                                    f"Clicked overlay/consent button: {btn_selector}"
                                )
                            except Exception:
                                pass
                except Exception as overlay_error:
                    logger.debug(f"Overlay/popup cleanup failed: {overlay_error}")
                # Handle consent screen overlay
                try:
                    consent_button = self.page.locator("button:has-text('Accept')")
                    if consent_button.is_visible():
                        consent_button.click()
                        logger.info("Dismissed consent screen overlay.")
                except Exception as consent_error:
                    logger.debug(f"Failed to dismiss consent screen: {consent_error}")
                # Close consent screen if visible
                try:
                    consent_button = self.page.locator("button", has_text="Consent")
                    if consent_button.is_visible():
                        consent_button.click()
                        logger.debug("Consent screen closed successfully.")
                except Exception as consent_error:
                    logger.debug(f"Failed to close consent screen: {consent_error}")
                # Additional strategy: Scroll into view before retrying
                try:
                    self.page.locator(selector).scroll_into_view_if_needed()
                    logger.debug(
                        f"Scrolled element '{selector}' into view before retrying click"
                    )
                except Exception as scroll_error:
                    logger.debug(f"Scrolling failed for '{selector}': {scroll_error}")
                # Capture screenshot for debugging
                try:
                    screenshot_path = f"debug_screenshot_{int(time.time())}.png"
                    self.page.screenshot(path=screenshot_path)
                    logger.debug(f"Screenshot captured: {screenshot_path}")
                except Exception as screenshot_error:
                    logger.debug(f"Failed to capture screenshot: {screenshot_error}")
                # Capture full page content for debugging
                page_content = self.page.content()
                logger.debug(f"Full page content: {page_content[:1000]}...")
                # Log the visibility state of the element
                is_visible = self.page.locator(selector).is_visible()
                logger.debug(f"Visibility state of '{selector}': {is_visible}")
                # Log the current DOM structure for debugging
                dom_snapshot = self.page.content()
                logger.debug(f"DOM snapshot captured: {dom_snapshot[:1000]}...")
                # Log network activity during retries
                try:
                    network_logs = self.page.evaluate(
                        "() => performance.getEntriesByType('resource')"
                    )
                    logger.debug(f"Network activity: {network_logs}")
                except Exception as network_error:
                    logger.debug(f"Failed to capture network activity: {network_error}")
                # Add a robust wait for dynamic content
                try:
                    self.page.wait_for_load_state("networkidle")
                    logger.debug("Page reached network idle state.")
                except Exception as load_error:
                    logger.debug(f"Failed to wait for network idle state: {load_error}")
                # Add explicit wait for the View Cart link
                refined_selector = "a[href='/view_cart']"
                # Increase timeout for waiting for the View Cart link
                try:
                    self.page.wait_for_selector(
                        refined_selector,
                        state="visible",
                        timeout=60000,  # Increased timeout
                    )
                    logger.debug(
                        "Refined selector: View Cart link is now visible after increased timeout."
                    )
                except Exception as refined_selector_error:
                    logger.debug(
                        f"Refined selector still failed for View Cart link after increased timeout: {refined_selector_error}"
                    )
                # Debugging for JavaScript errors
                try:
                    js_errors = self.page.evaluate("() => window.jsErrors")
                    if js_errors:
                        logger.debug(f"JavaScript errors detected: {js_errors}")
                    else:
                        logger.debug("No JavaScript errors detected.")
                except Exception as js_error_debug:
                    logger.debug(
                        f"Failed to capture JavaScript errors: {js_error_debug}"
                    )

                time.sleep(retry_delay)
                logger.debug(
                    f"Retrying click for '{selector}' after {retry_delay} seconds"
                )
                logger.debug(
                    f"Attempt {attempt}/{max_retries}: Retrying click for '{selector}'"
                )
                logger.debug(
                    "Attempting additional cleanup strategies before retrying..."
                )
                # Additional cleanup strategies can be added here
                continue
        logger.critical(
            f"Final attempt to click element '{selector}' failed after {max_retries} retries: {last_error}"
        )
        raise AssertionError(
            f"Unable to click element '{selector}' after {max_retries} attempts: {last_error}"
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
