"""
API Testing Utilities — reusable REST client with logging and validation.

Usage:
    api = APIUtils("https://api.example.com")
    response = api.get("/products")
    api.verify_status_code(response, 200)
"""

import json
import logging
import os
from typing import Dict, Optional, Union
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


class APIUtils:
    """
    REST client with session management, auth, logging and response validation.

    Attributes:
        base_url: Base URL for all API requests.
        session: Persistent ``requests.Session``.
        default_headers: Default HTTP headers sent with every request.
    """

    def __init__(self, base_url: str, default_headers: Optional[Dict] = None):
        """Create a new client. Defaults to JSON Content-Type / Accept headers."""
        self.base_url = base_url
        self.session = requests.Session()
        self.default_headers = default_headers or {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session.headers.update(self.default_headers)

    def set_auth_token(self, token: str, auth_type: str = "Bearer") -> None:
        """Set Authorization header for all subsequent requests."""
        self.session.headers.update({"Authorization": f"{auth_type} {token}"})

    @staticmethod
    def _safe_json(response: requests.Response) -> Union[dict, list, str]:
        """Return parsed JSON from *response*, or raw text on decode failure."""
        if not response.content:
            return {}
        try:
            return response.json()
        except (json.JSONDecodeError, ValueError):
            return response.text

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Send GET request. *params* are appended as query-string parameters."""
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"GET {url}")

        response = self.session.get(url, params=params, **kwargs)
        self._log_response(response)
        return response

    def post(
        self, endpoint: str, data: Optional[Union[Dict, str]] = None, **kwargs
    ) -> requests.Response:
        """Send POST request. *data* is serialised as JSON."""
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"POST {url}")

        response = self.session.post(url, json=data, **kwargs)
        self._log_response(response)
        return response

    def put(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Send PUT request. *data* is serialised as JSON."""
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"PUT {url}")

        response = self.session.put(url, json=data, **kwargs)
        self._log_response(response)
        return response

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Send DELETE request."""
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"DELETE {url}")

        response = self.session.delete(url, **kwargs)
        self._log_response(response)
        return response

    def patch(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Send PATCH request. *data* is serialised as JSON."""
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"PATCH {url}")

        response = self.session.patch(url, json=data, **kwargs)
        self._log_response(response)
        return response

    def _log_response(self, response: requests.Response) -> None:
        """Log status code, elapsed time, and first 500 chars of body."""
        try:
            response_data = response.json() if response.content else {}
            response_data_str = json.dumps(response_data, indent=2)[:500]  # Limit length
        except json.JSONDecodeError:
            response_data_str = response.text[:500]

        logger.info(
            f"Response - Status: {response.status_code}, Time: {response.elapsed.total_seconds():.2f}s"
        )
        logger.debug(f"Response Body: {response_data_str}")

    def verify_status_code(self, response: requests.Response, expected_code: int) -> None:
        """Assert the response status code equals *expected_code*."""
        assert (
            response.status_code == expected_code
        ), f"Expected status {expected_code}, got {response.status_code}. Response: {response.text}"

    def verify_response_schema(self, response: requests.Response, schema: Dict) -> None:
        """
        Basic schema check: verify each key exists and its value matches the expected type.

        For full JSON-Schema validation use the ``jsonschema`` library.
        """
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            raise AssertionError("Response is not valid JSON")

        # Basic schema validation (for full validation, consider using jsonschema library)
        for key, expected_type in schema.items():
            assert key in response_data, f"Missing key in response: {key}"
            assert isinstance(
                response_data[key], expected_type
            ), f"Key '{key}' should be {expected_type}, got {type(response_data[key])}"

    def save_response_to_file(self, response: requests.Response, file_path: str) -> None:
        """Dump status, headers and body as JSON to *file_path* (creates dirs)."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        response_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": self._safe_json(response),
        }

        with open(file_path, "w") as f:
            json.dump(response_data, f, indent=2)

        logger.info(f"Response saved to: {file_path}")

    def clear_auth(self) -> None:
        """Remove the Authorization header from the session."""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
            logger.debug("Cleared Authorization header")
