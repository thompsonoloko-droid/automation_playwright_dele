# conftest.py
"""
Pytest Configuration and Fixtures Module

This module provides pytest configuration and reusable fixtures for the automation
test suite. It handles:
- Playwright browser context and page setup
- Test data loading from JSON files
- Screenshot capture on test failures
- Video recording (optional)
- Test execution reporting and hooks
- Logging configuration

All fixtures are designed to be session/function scoped as appropriate and provide
a consistent testing environment across all test modules.

Key Fixtures:
- browser_context_args: Browser configuration (viewport, https, video)
- page: Browser page with automatic navigation to base URL
- test_data: Test credentials and data from JSON files
- cleanup_videos: Optional video cleanup after test pass
"""

import pytest
from playwright.sync_api import Page, BrowserContext
from typing import Dict, List
import logging
from datetime import datetime
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Configure logging for all test outputs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Ensure report directories exist before tests run
REPORT_DIRS = ["./reports/screenshots", "./reports/videos", "./reports/allure-results"]
for report_dir in REPORT_DIRS:
    os.makedirs(report_dir, exist_ok=True)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configure Playwright browser context arguments.

    This fixture customizes the browser context settings for all tests, ensuring consistent behavior.

    Customizations include:
    - Setting a fixed viewport size for uniform rendering.
    - Ignoring HTTPS errors to handle self-signed certificates.
    - Optional video recording (disabled by default).

    Args:
        browser_context_args (dict): Default browser context arguments provided by pytest-playwright.

    Returns:
        dict: Updated browser context configuration.

    Note:
        Uncomment the 'record_video_dir' line to enable video recording for all tests.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        # Uncomment the line below to enable video recording for "ALL" tests:
        # "record_video_dir": "./reports/videos"
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    """
    Create a new browser page for each test with automatic setup.

    This fixture ensures test isolation by creating a fresh browser page for each test.
    It also handles:
    - Navigation to the base URL.
    - Automatic dismissal of consent/cookie dialogs.
    - Screenshot capture on test failure.
    - Cleanup of the page after test completion.

    Args:
        context (BrowserContext): Playwright BrowserContext provided by pytest-playwright.
        request (FixtureRequest): Pytest request object containing test metadata.

    Yields:
        Page: Playwright Page object ready for automation.

    Raises:
        Exception: If navigation to the base URL fails.

    Example:
        def test_login(page):
            page.goto("https://automationexercise.com")
    """
    page = context.new_page()
    base_url = "https://automationexercise.com/"
    try:
        page.goto(base_url, wait_until="domcontentloaded", timeout=30000)
    except Exception as e:
        logging.error(f"Failed to navigate to {base_url}: {e}")
        page.close()
        raise

    yield page

    rep = getattr(request.node, "rep_call", None)
    if rep and getattr(rep, "failed", False):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = (
            f"./reports/screenshots/failure_{request.node.name}_{timestamp}.png"
        )
        page.screenshot(path=screenshot_path)
        logging.error(f"Test failed. Screenshot saved: {screenshot_path}")
    page.close()


@pytest.fixture(scope="function")
def test_data():
    """
    Load test data from a JSON file or use fallback data.

    This fixture provides test credentials and data for parameterized testing.
    It supports backward compatibility with multiple data formats.

    Returns:
        list: A list of dictionaries containing valid and invalid user credentials.

    Example:
        def test_login(test_data):
            user = test_data[0]['valid_user']
            email = user['email']

    Note:
        If the test_data.json file is missing, the fixture uses default fallback data
        with dynamically generated test user emails.
    """
    test_data_path = os.path.join(
        os.path.dirname(__file__), "..", "test_data", "test_data.json"
    )

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
        with open(test_data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback_data


@pytest.fixture(scope="function")
def cleanup_videos(request):
    """
    Delete video files for passing tests to save disk space.

    Saves disk space by automatically removing video recordings
    for tests that passed (failed test videos are kept for debugging).

    Usage:
        Add 'cleanup_videos' parameter to test function to enable:

        def test_example(cleanup_videos):
            # Test code here
            # Video will be deleted if test passes

    Example:
        @pytest.mark.parametrize("data", [...])
        def test_with_cleanup(cleanup_videos, data):
            assert True  # Video deleted if passed
    """
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.passed:
        video_dir = Path("./reports/videos")
        for video_file in video_dir.glob(f"*{request.node.name}*.webm"):
            video_file.unlink(missing_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture test execution reports for use in fixtures.

    This hook is called for each test phase (setup, call, teardown).
    It captures the test result and makes it available to other fixtures.

    Used by:
    - page fixture to capture screenshots on failure
    - cleanup_videos fixture to check test result

    Args:
        item: Pytest test item
        call: Pytest call object with test execution info

    Note:
        This is a pytest hook and is called automatically.
        No need to call directly in tests.
    """
    outcome = yield
    setattr(item, f"rep_{outcome.get_result().when}", outcome.get_result())
