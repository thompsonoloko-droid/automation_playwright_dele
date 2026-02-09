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

    Sets up common browser configurations for all tests:
    - Viewport size for consistent rendering
    - HTTPS error ignoring for self-signed certificates
    - Optional video recording (commented out by default)

    Args:
        browser_context_args: Default browser context arguments from pytest-playwright

    Returns:
        dict: Updated browser context configuration

    Note:
        To enable video recording for all tests, uncomment the 'record_video_dir' line.
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

    This fixture:
    1. Creates a fresh page instance for test isolation
    2. Navigates to the base URL
    3. Handles consent/cookie dialogs automatically
    4. Captures screenshots on test failure
    5. Cleans up the page after test completion

    Args:
        context: Playwright BrowserContext from pytest-playwright
        request: Pytest request object for test info

    Yields:
        Page: Playwright Page object ready for automation

    Raises:
        Exception: If unable to navigate to base URL

    Example:
        def test_login(page):
            page.goto("https://automationexercise.com")
    """
    page = context.new_page()
    test_name = request.node.name
    test_logger = logging.getLogger(test_name)

    # Navigate to base URL with timeout
    base_url = "https://automationexercise.com/"
    try:
        page.goto(base_url, wait_until="domcontentloaded", timeout=30000)
        test_logger.info(f"Navigated to {base_url}")

        # Try to close any consent dialogs
        try:
            # Multiple strategies to close consent
            page.wait_for_timeout(500)

            # Try pressing Escape multiple times
            for _ in range(3):
                page.press("body", "Escape")
                page.wait_for_timeout(100)

            # Try clicking Consent button if it exists
            try:
                page.click("button:has-text('Consent')", timeout=2000, force=True)
            except:
                pass

            # Try removing the overlay with JavaScript
            try:
                page.evaluate(
                    """
                    const overlay = document.querySelector('[class*="fc-consent"], [class*="cookiebot"]');
                    if (overlay) overlay.remove();
                """
                )
            except:
                pass

            page.wait_for_timeout(500)
        except:
            pass

    except Exception as e:
        test_logger.error(f"Failed to navigate to {base_url}: {str(e)}")
        page.close()
        raise

    yield page

    # Capture screenshot on failure
    try:
        rep = getattr(request.node, "rep_call", None)
        if rep and hasattr(rep, "failed") and rep.failed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = (
                f"./reports/screenshots/failure_{test_name}_{timestamp}.png"
            )
            page.screenshot(path=screenshot_path)
            test_logger.error(f"Test failed. Screenshot saved: {screenshot_path}")
    except Exception as screenshot_error:
        test_logger.warning(f"Failed to capture screenshot: {str(screenshot_error)}")
    finally:
        # Try to close the page, ignoring any errors to prevent test failures during teardown
        if page:
            try:
                page.close()
            except KeyboardInterrupt:
                pass  # Ignore KeyboardInterrupt during cleanup
            except Exception:
                pass  # Silently ignore all other errors during page close


@pytest.fixture(scope="function")
def test_data():
    """
    Load test data from JSON file with fallback defaults.

    Loads test credentials and data from test_data/test_data.json.
    Provides backward compatibility with multiple data formats.

    Returns:
        list: Test data list with valid and invalid user credentials

    Structure:
        If JSON format is {"users": [...], "invalid_credentials": [...]}:
            Returns: [{"valid_user": {...}, "invalid_user": {...}}]

        Otherwise returns data as-is for backward compatibility

    Example:
        def test_login(test_data):
            user = test_data[0]['valid_user']
            email = user['email']

    Note:
        If test_data.json is missing, uses default fallback data
        with dynamically generated test user email (timestamp-based)
    """
    test_data_path = os.path.join(
        os.path.dirname(__file__), "..", "test_data", "test_data.json"
    )

    # Fallback data for backward compatibility
    fallback_data = [
        {
            "valid_user": {
                "name": "Test User",
                "email": f"testuser_{int(datetime.now().timestamp())}@example.com",
            },
            "invalid_user": {"name": "", "email": ""},
        }
    ]

    try:
        if os.path.exists(test_data_path):
            with open(test_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info(f"Test data loaded from {test_data_path}")
                # For backward compatibility with tests expecting [{"valid_user": {}}] format
                if "users" in data and "invalid_credentials" in data:
                    # New format - wrap for backward compatibility
                    valid_user = data["users"][0] if data["users"] else {}
                    invalid_cred = (
                        data["invalid_credentials"][0]
                        if data["invalid_credentials"]
                        else {}
                    )
                    return [{"valid_user": valid_user, "invalid_user": invalid_cred}]
                else:
                    # Old format - return as-is
                    return data if isinstance(data, list) else [data]
        else:
            logger.warning(
                f"Test data file not found: {test_data_path}. Using defaults."
            )
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to load test data: {str(e)}. Using defaults.")

    return fallback_data


@pytest.fixture(scope="function")
def cleanup_videos(request):
    """
    Optional fixture to delete video files from passing tests.

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

    # Only delete videos if test passed
    if request.node.rep_call.passed if hasattr(request.node, "rep_call") else True:
        video_dir = Path("./reports/videos")
        if video_dir.exists():
            test_name = request.node.name
            # Find and delete video files for this test
            for video_file in video_dir.glob(f"*{test_name}*.webm"):
                try:
                    video_file.unlink()
                    logger.debug(f"Deleted video: {video_file}")
                except Exception as e:
                    logger.warning(f"Failed to delete video {video_file}: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture test execution reports.

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
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
