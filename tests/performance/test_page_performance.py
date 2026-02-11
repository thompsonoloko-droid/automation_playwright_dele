# tests/performance/test_page_performance.py
"""
UI Page Load Performance Tests (Data-Driven)

Verifies that key pages load within acceptable time thresholds using
Playwright's Navigation Timing API and Performance metrics.

Pages and thresholds are configured in test_data/test_data.json → performance.pages.

Example:
    pytest tests/performance/test_page_performance.py -v
    pytest -m performance -v
"""

import json
import logging
from pathlib import Path

import pytest
from playwright.sync_api import Page

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
_DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "test_data.json"
_SITE_URL = "https://automationexercise.com"


def _load_perf_config() -> dict:
    """Load the 'performance' section from test_data.json."""
    with open(_DATA_FILE) as f:
        return json.load(f)["performance"]


def _pages() -> list[tuple[str, str, int]]:
    """Return parametrize-ready tuples (name, path, max_ms) for page load tests."""
    cfg = _load_perf_config()
    return [(p["name"], p["path"], p["max_ms"]) for p in cfg["pages"]]


GLOBAL_MAX_MS = _load_perf_config()["page_load_time_ms"]


class TestPageLoadPerformance:
    """Data-driven page load performance tests using Playwright."""

    @pytest.mark.performance
    @pytest.mark.ui
    @pytest.mark.parametrize("name,path,max_ms", _pages(), ids=[p[0] for p in _pages()])
    def test_page_load_time(self, page: Page, name: str, path: str, max_ms: int):
        """
        Verify a page loads within the configured threshold.

        Uses the Navigation Timing API (domContentLoadedEventEnd - navigationStart)
        for an accurate browser-measured load time.
        """
        url = f"{_SITE_URL}{path}"

        # Navigate and wait for DOM content loaded
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # Measure via Navigation Timing Level 2 API (L1 performance.timing is deprecated)
        timing = page.evaluate(
            """() => {
            const [entry] = performance.getEntriesByType('navigation');
            return {
                domContentLoadedMs: Math.round(entry.domContentLoadedEventEnd - entry.startTime),
                fullLoadMs: Math.round(entry.loadEventEnd - entry.startTime),
                firstByte: Math.round(entry.responseStart - entry.startTime),
                domInteractive: Math.round(entry.domInteractive - entry.startTime)
            };
        }"""
        )

        dom_loaded_ms = timing["domContentLoadedMs"]
        ttfb_ms = timing["firstByte"]
        dom_interactive_ms = timing["domInteractive"]

        assert (
            dom_loaded_ms < max_ms
        ), f"[{name}] DOM content loaded in {dom_loaded_ms}ms, exceeded {max_ms}ms threshold"

        logger.info(
            f"✓ {name}: TTFB={ttfb_ms}ms  DOMInteractive={dom_interactive_ms}ms  "
            f"DOMContentLoaded={dom_loaded_ms}ms  (threshold: {max_ms}ms)"
        )

    @pytest.mark.performance
    @pytest.mark.ui
    def test_homepage_resource_count(self, page: Page):
        """
        Verify the homepage doesn't load an excessive number of resources.

        A high resource count can indicate performance issues (unoptimized
        assets, too many third-party scripts, etc.).
        """
        page.goto(f"{_SITE_URL}/", wait_until="load", timeout=60000)

        resource_count = page.evaluate(
            "() => performance.getEntriesByType('resource').length"
        )
        total_size_kb = page.evaluate(
            """() => {
            const entries = performance.getEntriesByType('resource');
            return Math.round(entries.reduce((sum, e) => sum + (e.transferSize || 0), 0) / 1024);
        }"""
        )

        # Soft threshold — log a warning if over 100 resources but don't fail
        if resource_count > 100:
            logger.warning(
                f"Homepage loaded {resource_count} resources ({total_size_kb}KB) — consider optimizing"
            )
        else:
            logger.info(
                f"✓ Homepage resources: {resource_count} files, {total_size_kb}KB transferred"
            )

        # Hard limit — fail if wildly excessive
        assert (
            resource_count < 200
        ), f"Homepage loaded {resource_count} resources — likely a performance issue"

    @pytest.mark.performance
    @pytest.mark.ui
    def test_no_large_layout_shifts(self, page: Page):
        """
        Verify the homepage does not have excessive Cumulative Layout Shift (CLS).

        Uses the Layout Instability API to measure CLS. A CLS > 0.25 indicates
        a poor user experience with elements jumping around during load.
        """
        page.goto(f"{_SITE_URL}/", wait_until="load", timeout=60000)
        page.wait_for_timeout(2000)  # Allow late-loading content to settle

        cls_score = page.evaluate(
            """() => {
            return new Promise(resolve => {
                let cls = 0;
                const observer = new PerformanceObserver(list => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) cls += entry.value;
                    }
                });
                observer.observe({ type: 'layout-shift', buffered: true });
                // Give observer time to process buffered entries
                setTimeout(() => {
                    observer.disconnect();
                    resolve(Math.round(cls * 1000) / 1000);
                }, 500);
            });
        }"""
        )

        cls_threshold = _load_perf_config().get("cls_threshold", 0.35)
        assert (
            cls_score < cls_threshold
        ), f"CLS score {cls_score} exceeds {cls_threshold} threshold (poor experience)"

        if cls_score < 0.1:
            logger.info(f"✓ CLS score: {cls_score} (good)")
        elif cls_score < 0.25:
            logger.info(f"✓ CLS score: {cls_score} (needs improvement, target < 0.1)")
        else:
            logger.warning(
                f"CLS score: {cls_score} (acceptable but high, threshold: {cls_threshold})"
            )
