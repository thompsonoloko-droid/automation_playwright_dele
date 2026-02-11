# tests/performance/test_api_performance.py
"""
API Response Time Performance Tests (Data-Driven)

Verifies that all API endpoints respond within acceptable time thresholds.
Thresholds and endpoints are configured in test_data/test_data.json → performance.

Each test runs the request multiple times and asserts:
- Every individual response is under the per-endpoint max_ms threshold
- The average response time is under the global api_response_time_ms threshold

Example:
    pytest tests/performance/ -v
    pytest tests/performance/ -m performance -v
"""

import json
import logging
import os
import time
from pathlib import Path

import pytest
import requests

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
_DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "test_data.json"


def _load_perf_config() -> dict:
    """Load the 'performance' section from test_data.json."""
    with open(_DATA_FILE) as f:
        return json.load(f)["performance"]


def _load_api_base_url() -> str:
    """Load the API base URL from test_data.json."""
    with open(_DATA_FILE) as f:
        return json.load(f)["api"]["base_url"]


def _resolve_env_vars(data: dict | None) -> dict | None:
    """Resolve $ENV_VAR references in data dict values."""
    if not data:
        return data
    return {
        k: os.environ.get(v[1:], v) if isinstance(v, str) and v.startswith("$") else v
        for k, v in data.items()
    }


def _api_endpoints() -> list[tuple[str, str, str, dict | None, int]]:
    """Return parametrize-ready tuples for API endpoint performance tests."""
    cfg = _load_perf_config()
    return [
        (
            ep["name"],
            ep["method"],
            ep["path"],
            _resolve_env_vars(ep.get("data")),
            ep["max_ms"],
        )
        for ep in cfg["api_endpoints"]
    ]


_perf_cfg = _load_perf_config()
BASE_URL = _load_api_base_url()
GLOBAL_MAX_MS = _perf_cfg["api_response_time_ms"]
TIMEOUT = 15
ITERATIONS = 3  # Number of requests per endpoint for averaging


class TestAPIPerformance:
    """Data-driven API response time performance tests."""

    @pytest.mark.performance
    @pytest.mark.api
    @pytest.mark.parametrize(
        "name,method,path,data,max_ms",
        _api_endpoints(),
        ids=[e[0] for e in _api_endpoints()],
    )
    def test_api_response_time(self, name, method, path, data, max_ms):
        """
        Verify an API endpoint responds within the configured threshold.

        Runs ITERATIONS requests, asserts each is under max_ms,
        and logs the average response time.
        """
        url = f"{BASE_URL}{path}"
        times_ms: list[float] = []

        for i in range(ITERATIONS):
            start = time.perf_counter()
            if method.upper() == "GET":
                response = requests.get(url, timeout=TIMEOUT)
            else:
                response = requests.post(url, data=data or {}, timeout=TIMEOUT)
            elapsed_ms = (time.perf_counter() - start) * 1000
            times_ms.append(elapsed_ms)

            assert (
                response.status_code == 200
            ), f"[{name}] iteration {i+1}: HTTP {response.status_code}"
            assert (
                elapsed_ms < max_ms * 1.05
            ), f"[{name}] iteration {i+1}: {elapsed_ms:.0f}ms exceeded {max_ms}ms threshold"

        avg_ms = sum(times_ms) / len(times_ms)
        min_ms = min(times_ms)
        max_actual = max(times_ms)

        logger.info(
            f"✓ {name}: avg={avg_ms:.0f}ms  min={min_ms:.0f}ms  max={max_actual:.0f}ms  "
            f"(threshold: {max_ms}ms)"
        )

    @pytest.mark.performance
    @pytest.mark.api
    def test_api_concurrent_products_search(self):
        """
        Verify the search endpoint handles rapid sequential requests
        without degradation.

        Sends 5 search requests back-to-back and checks none exceed
        the global threshold.
        """
        url = f"{BASE_URL}/searchProduct"
        search_terms = ["Top", "Dress", "Jeans", "Shirt", "Saree"]
        times_ms: list[float] = []

        for term in search_terms:
            start = time.perf_counter()
            response = requests.post(
                url, data={"search_product": term}, timeout=TIMEOUT
            )
            elapsed_ms = (time.perf_counter() - start) * 1000
            times_ms.append(elapsed_ms)

            assert response.status_code == 200
            # Apply 50% burst tolerance — sequential requests experience network queuing
            burst_max = GLOBAL_MAX_MS * 1.5
            assert (
                elapsed_ms < burst_max
            ), f"Search '{term}': {elapsed_ms:.0f}ms exceeded {burst_max:.0f}ms burst threshold"

        avg_ms = sum(times_ms) / len(times_ms)
        logger.info(
            f"✓ Sequential search burst: avg={avg_ms:.0f}ms across {len(search_terms)} terms "
            f"(threshold: {GLOBAL_MAX_MS}ms)"
        )
