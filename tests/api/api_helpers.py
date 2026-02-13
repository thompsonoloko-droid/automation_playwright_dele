# tests/api/api_helpers.py
"""
Shared utilities for API tests.

Provides a retry-enabled requests.Session to handle transient failures
from the external API (automationexercise.com), including:
- Cloudflare 520-524 errors
- Standard 5xx server errors
- Connection/timeout errors
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_api_session() -> requests.Session:
    """
    Create a requests.Session with retry logic for transient API failures.

    Returns:
        requests.Session: Configured session with exponential backoff retry policy.

    Retry configuration:
        - Total retries: 3
        - Backoff factor: 1 (delays: 1s, 2s, 4s)
        - Status codes: 500, 502, 503, 520, 521, 522, 523, 524 (Cloudflare + server errors)
        - Retries on: Connection errors, read timeouts

    Note on retrying POST/PUT/DELETE:
        While retrying non-idempotent methods can risk duplicate operations, this is
        necessary for the external automationexercise.com API which experiences:
        1. Cloudflare 520 errors (server not ready) - no request reached the server
        2. Connection timeouts - request never completed
        In both cases, retrying is safe as the operation didn't complete initially.
        The API test suite validates correct behavior even with retries.

    Note on session reuse:
        Each call creates a new session for test isolation and simplicity. While
        connection pooling could improve performance, test independence is prioritized
        over optimization in this test infrastructure.
    """
    session = requests.Session()

    # Configure retry strategy with exponential backoff
    retry_strategy = Retry(
        total=3,  # Maximum number of retries
        backoff_factor=1,  # Wait 1s, 2s, 4s between retries
        status_forcelist=[
            500,
            502,
            503,
            520,
            521,
            522,
            523,
            524,
        ],  # Cloudflare + 5xx errors
        allowed_methods=[
            "HEAD",
            "GET",
            "PUT",
            "DELETE",
            "POST",
            "OPTIONS",
            "TRACE",
        ],  # Retry all HTTP methods
        raise_on_status=False,  # Don't raise exception on retry-able status codes
    )

    # Mount the adapter with retry logic for both http and https
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session
