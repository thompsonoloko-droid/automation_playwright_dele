"""
Shared fixtures and constants for API tests.

Centralises config loading so individual test modules can simply::

    from tests.api.conftest import BASE_URL, TIMEOUT
"""

import json
import logging
import os
from pathlib import Path

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

_DATA_FILE = Path(__file__).resolve().parent.parent.parent / "test_data" / "test_data.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_test_data() -> dict:
    """Return the full parsed contents of test_data.json."""
    with open(_DATA_FILE) as f:
        return json.load(f)


def _load_api_config() -> dict:
    """Return only the ``api`` section of test_data.json."""
    return _load_test_data()["api"]


def _resolve_env(value: str) -> str:
    """If *value* starts with ``$``, resolve it from the environment."""
    if isinstance(value, str) and value.startswith("$"):
        return os.environ.get(value[1:], value)
    return value


# ---------------------------------------------------------------------------
# Module-level constants (importable by test files)
# ---------------------------------------------------------------------------

_cfg = _load_api_config()
BASE_URL: str = _cfg["base_url"]
TIMEOUT: int = _cfg["timeout"]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def api_config() -> dict:
    """Session-scoped fixture that returns the ``api`` config dict."""
    return _cfg


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    """Session-scoped ``requests.Session`` with retry logic for transient failures.

    Retry configuration:
        - Total retries: 3
        - Backoff factor: 1 (delays: 1s, 2s, 4s)
        - Status codes: 500, 502, 503, 520-524 (Cloudflare + server errors)
        - Retries on: Connection errors (incl. SSL), read timeouts
    """
    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )

    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 520, 521, 522, 523, 524],
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "POST", "OPTIONS", "TRACE"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    yield session
    session.close()
