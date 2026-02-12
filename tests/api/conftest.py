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
    """Session-scoped fixture that returns a shallow copy of the ``api`` config dict.
    
    Note: This is a shallow copy to prevent test pollution at the top level.
    _cfg does not contain nested dicts, so shallow copy is sufficient.
    """
    return _cfg.copy()


@pytest.fixture(scope="session")
def api_session() -> requests.Session:
    """Session-scoped ``requests.Session`` pre-configured with JSON headers."""
    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    yield session
    session.close()
