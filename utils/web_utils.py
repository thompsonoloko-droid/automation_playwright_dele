# web_utils.py
"""Playwright helper utilities — click, fill, wait, scroll, screenshot, etc."""

import logging
import time
import warnings
from typing import List, Optional

from playwright.sync_api import Locator, Page

logger = logging.getLogger(__name__)


class WebUtils:
    """Convenience wrappers around Playwright's Page API with built-in waits and logging.

    .. deprecated::
        This class is not currently used by any test or page object.
        Prefer using methods on :class:`pages.base_page.BasePage` instead.
        Retained for reference; may be removed in a future cleanup.
    """

    def __init__(self, page: Page):
        """Wrap a Playwright Page instance."""
        warnings.warn(
            "WebUtils is deprecated — use BasePage helpers instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.page = page

    def wait_and_click(self, selector: str, timeout: int = 30000) -> None:
        """Wait for element to be visible, then click it."""
        try:
            element = self.page.locator(selector).first
            element.wait_for(state="visible", timeout=timeout)
            element.click()
            logger.debug(f"Clicked element: {selector}")
        except Exception as e:
            logger.error(f"Failed to click element {selector}: {e}")
            raise

    def fill_field(self, selector: str, text: str, timeout: int = 30000) -> None:
        """Wait for input to be visible and fill it with *text*."""
        try:
            element = self.page.locator(selector).first
            element.wait_for(state="visible", timeout=timeout)
            element.fill(text)
            logger.debug(f"Filled field {selector} with: {text}")
        except Exception as e:
            logger.error(f"Failed to fill field {selector}: {e}")
            raise

    def get_element_text(self, selector: str, timeout: int = 30000) -> str:
        """Return trimmed text content of the first matching element."""
        try:
            element = self.page.locator(selector).first
            element.wait_for(state="visible", timeout=timeout)
            text = element.text_content()
            return text.strip() if text else ""
        except Exception as e:
            logger.error(f"Failed to get text from {selector}: {e}")
            raise

    def take_screenshot(self, name: Optional[str] = None) -> str:
        """Save a screenshot to reports/screenshots/ and return the file path."""
        if not name:
            name = f"screenshot_{int(time.time())}"

        screenshot_path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    def wait_for_url_contains(self, text: str, timeout: int = 30000) -> None:
        """Block until the current URL contains *text*."""
        try:
            self.page.wait_for_url(f"**{text}**", timeout=timeout)
        except Exception as e:
            logger.error(f"URL did not contain '{text}' within {timeout}ms: {e}")
            raise

    def scroll_to_element(self, selector: str) -> None:
        """Scroll the first matching element into the viewport."""
        element = self.page.locator(selector).first
        element.scroll_into_view_if_needed()

    def get_all_elements(self, selector: str) -> List[Locator]:
        """Return all Locator objects matching *selector*."""
        return self.page.locator(selector).all()

    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Return True if the element is visible within *timeout* ms, else False."""
        try:
            self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def refresh_page(self) -> None:
        """Reload the page and wait for network idle."""
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

    def go_back(self) -> None:
        """Navigate back one page and wait for network idle."""
        self.page.go_back()
        self.page.wait_for_load_state("networkidle")
