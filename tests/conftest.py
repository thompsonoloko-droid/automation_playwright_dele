# conftest.py
"""
Pytest fixtures and hooks shared across all tests.

Key fixtures:
  - browser_context_args — viewport, HTTPS settings, optional video recording
  - page — fresh Playwright page pre-navigated to the base URL,
           with consent/cookie overlays blocked at the network level
  - test_data — loads test credentials from test_data/test_data.json
  - cleanup_videos — deletes video recordings for passing tests
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import BrowserContext

# Load .env from project root before any tests run (git-ignored, safe for secrets)
load_dotenv(Path(__file__).parent.parent / ".env")

logger = logging.getLogger(__name__)

# Configure logging for all test outputs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Ensure report output directories exist
REPORT_DIRS = ["./reports/screenshots", "./reports/videos", "./reports/allure-results"]
for report_dir in REPORT_DIRS:
    os.makedirs(report_dir, exist_ok=True)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Customise the Playwright browser context for all tests.

    Settings:
      - 1920×1080 viewport for consistent rendering.
      - HTTPS errors ignored (handles self-signed certs).
      - Video recording disabled by default (uncomment to enable).
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        # Uncomment to record video for every test:
        # "record_video_dir": "./reports/videos"
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    """
    Yield a fresh Playwright page for each test.

    Setup:
      1. Block consent-SDK network requests (fundingchoices, googleads).
      2. Inject a MutationObserver that removes any consent overlays.
      3. Navigate to https://automationexercise.com/.

    Teardown:
      - Captures a screenshot if the test failed.
      - Closes the page.
    """
    page = context.new_page()

    # Block consent/cookie SDK at the network level so overlays never appear
    page.route("**/*fundingchoices*/**", lambda route: route.abort())
    page.route("**/*fc.yahoo*/**", lambda route: route.abort())
    page.route("**/fundingchoicesmessages*", lambda route: route.abort())
    page.route("**/*googleads*/**", lambda route: route.abort())

    # Fallback: remove any consent overlays that bypass network blocking
    page.add_init_script(
        """
        const observer = new MutationObserver(() => {
            document.querySelectorAll('.fc-consent-root, .fc-dialog-overlay')
                .forEach(el => el.remove());
        });
        observer.observe(document.documentElement, { childList: true, subtree: true });
    """
    )

    base_url = os.environ.get("BASE_URL", "https://automationexercise.com/")
    try:
        page.goto(base_url, wait_until="domcontentloaded", timeout=60000)
    except Exception as e:
        logging.error(f"Failed to navigate to {base_url}: {e}")
        page.close()
        raise

    yield page

    rep = getattr(request.node, "rep_call", None)
    if rep and getattr(rep, "failed", False):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"./reports/screenshots/failure_{request.node.name}_{timestamp}.png"
        page.screenshot(path=screenshot_path)
        logging.error(f"Test failed. Screenshot saved: {screenshot_path}")
    page.close()


@pytest.fixture(scope="function")
def test_data():
    """
    Load test data from test_data/test_data.json.

    Returns a list of dicts for backward-compatible parametrisation.
    Falls back to dummy data if the JSON file is missing.
    """
    test_data_path = os.path.join(os.path.dirname(__file__), "..", "test_data", "test_data.json")

    fallback_data = [
        {
            "valid_user": {"name": "Test User", "email": "test@example.com"},
            "invalid_user": {"name": "Invalid User", "email": "invalid@example.com"},
        }
    ]

    if os.path.exists(test_data_path):
        with open(test_data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Normalize to always return a list for backward compatibility
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        # Fallback if the file content is not in an expected format
        return fallback_data
    return fallback_data


@pytest.fixture(scope="function")
def cleanup_videos(request):
    """
    Auto-delete video recordings for passing tests to save disk space.

    Usage: add ``cleanup_videos`` as a test parameter to opt in.
    """
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.passed:
        video_dir = Path("./reports/videos")
        if video_dir.exists():
            for video_file in video_dir.glob("*.webm"):
                video_file.unlink(missing_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store each test phase result (setup/call/teardown) on the item for use by fixtures."""
    outcome = yield
    setattr(item, f"rep_{outcome.get_result().when}", outcome.get_result())
