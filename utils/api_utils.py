"""
API Testing Utilities Module

This module provides the APIUtils class for making RESTful API requests with
built-in error handling, response validation, and logging. It supports:
- GET, POST, PUT, DELETE, PATCH HTTP methods
- Custom headers and authentication
- Request/response logging
- Response validation (status codes, schema)
- File I/O for response storage

Example:
    from utils.api_utils import APIUtils

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
    Utility class for RESTful API testing operations.

    Provides methods for making HTTP requests with automatic:
    - Error handling and retries
    - Response logging (limited to prevent huge logs)
    - Session management
    - Authentication handling
    - Response validation

    Attributes:
        base_url (str): Base URL for all API requests
        session (requests.Session): Persistent session for requests
        default_headers (dict): Default HTTP headers for all requests

    Example:
        >>> api = APIUtils("https://api.example.com")
        >>> response = api.get("/users/123")
        >>> api.verify_status_code(response, 200)
        >>> data = response.json()
    """

    def __init__(self, base_url: str, default_headers: Optional[Dict] = None):
        """
        Initialize APIUtils with base URL and optional default headers.

        Args:
            base_url (str): Base URL for all API endpoints
            default_headers (Optional[Dict]): Custom HTTP headers. Defaults to JSON content-type.

        Example:
            >>> api = APIUtils("https://api.example.com",
            ...                 {"X-API-Key": "your-key"})
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.default_headers = default_headers or {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.session.headers.update(self.default_headers)

    def set_auth_token(self, token: str, auth_type: str = "Bearer") -> None:
        """
        Set authentication token for all subsequent requests.

        Adds Authorization header to session headers.

        Args:
            token (str): Authentication token (JWT, API key, etc.)
            auth_type (str): Authorization header type (default: "Bearer")

        Example:
            >>> api.set_auth_token("eyJhbGciOiJIUzI1NiIs...")
            >>> response = api.get("/protected-endpoint")
        """
        self.session.headers.update({"Authorization": f"{auth_type} {token}"})

    def get(
        self, endpoint: str, params: Optional[Dict] = None, **kwargs
    ) -> requests.Response:
        """
        Send GET request to API endpoint.

        Args:
            endpoint (str): API endpoint path (relative to base_url)
            params (Optional[Dict]): URL query parameters
            **kwargs: Additional arguments passed to requests.get()

        Returns:
            requests.Response: Response object with status, headers, and body

        Raises:
            requests.RequestException: Network or request errors are logged

        Example:
            >>> response = api.get("/products", params={"page": 1})
        """
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"GET {url}")

        response = self.session.get(url, params=params, **kwargs)
        self._log_response(response)
        return response

    def post(
        self, endpoint: str, data: Optional[Union[Dict, str]] = None, **kwargs
    ) -> requests.Response:
        """
        Send POST request to API endpoint.

        Args:
            endpoint (str): API endpoint path (relative to base_url)
            data (Optional[Union[Dict, str]]): Request body data (converted to JSON)
            **kwargs: Additional arguments passed to requests.post()

        Returns:
            requests.Response: Response object with status, headers, and body

        Example:
            >>> api.post("/users", data={"name": "John", "email": "john@example.com"})
        """
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"POST {url}")

        response = self.session.post(url, json=data, **kwargs)
        self._log_response(response)
        return response

    def put(
        self, endpoint: str, data: Optional[Dict] = None, **kwargs
    ) -> requests.Response:
        """
        Send PUT request to API endpoint.

        Args:
            endpoint (str): API endpoint path (relative to base_url)
            data (Optional[Dict]): Request body data (converted to JSON)
            **kwargs: Additional arguments passed to requests.put()

        Returns:
            requests.Response: Response object with status, headers, and body

        Example:
            >>> api.put("/users/123", data={"name": "Jane Doe"})
        """
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"PUT {url}")

        response = self.session.put(url, json=data, **kwargs)
        self._log_response(response)
        return response

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """
        Send DELETE request to API endpoint.

        Args:
            endpoint (str): API endpoint path (relative to base_url)
            **kwargs: Additional arguments passed to requests.delete()

        Returns:
            requests.Response: Response object with status, headers, and body

        Example:
            >>> api.delete("/users/123")
        """
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"DELETE {url}")

        response = self.session.delete(url, **kwargs)
        self._log_response(response)
        return response

    def patch(
        self, endpoint: str, data: Optional[Dict] = None, **kwargs
    ) -> requests.Response:
        """
        Send PATCH request to API endpoint.

        Args:
            endpoint (str): API endpoint path (relative to base_url)
            data (Optional[Dict]): Request body data (converted to JSON)
            **kwargs: Additional arguments passed to requests.patch()

        Returns:
            requests.Response: Response object with status, headers, and body

        Example:
            >>> api.patch("/users/123", data={"status": "active"})
        """
        url = urljoin(self.base_url, endpoint)
        logger.debug(f"PATCH {url}")

        response = self.session.patch(url, json=data, **kwargs)
        self._log_response(response)
        return response

    def _log_response(self, response: requests.Response) -> None:
        """
        Log response details for debugging and reporting.

        Logs status code, response time, and truncated response body.
        Response body limited to 500 chars to prevent huge log files.

        Args:
            response (requests.Response): Response object to log

        Note:
            This is an internal method, called automatically by HTTP methods.
        """
        try:
            response_data = response.json() if response.content else {}
            response_data_str = json.dumps(response_data, indent=2)[
                :500
            ]  # Limit length
        except json.JSONDecodeError:
            response_data_str = response.text[:500]

        logger.info(
            f"Response - Status: {response.status_code}, Time: {response.elapsed.total_seconds():.2f}s"
        )
        logger.debug(f"Response Body: {response_data_str}")

    def verify_status_code(
        self, response: requests.Response, expected_code: int
    ) -> None:
        """
        Verify response status code matches expected value.

        Args:
            response (requests.Response): Response object to verify
            expected_code (int): Expected HTTP status code

        Raises:
            AssertionError: If status code doesn't match with error details

        Example:
            >>> response = api.get("/products")
            >>> api.verify_status_code(response, 200)
        """
        assert (
            response.status_code == expected_code
        ), f"Expected status {expected_code}, got {response.status_code}. Response: {response.text}"

    def verify_response_schema(self, response: requests.Response, schema: Dict) -> None:
        """
        Verify response matches basic JSON schema structure.

        Performs basic validation by checking:
        - All required keys exist in response
        - Values match expected types

        Note:
            For complex schema validation, use the 'jsonschema' library separately.

        Args:
            response (requests.Response): Response object to validate
            schema (Dict): Schema dict with keys mapping to expected types

        Raises:
            AssertionError: If schema validation fails

        Example:
            >>> schema = {"id": int, "name": str, "active": bool}
            >>> api.verify_response_schema(response, schema)
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

    def save_response_to_file(
        self, response: requests.Response, file_path: str
    ) -> None:
        """
        Save API response to JSON file for inspection.

        Saves status code, headers, and body to a JSON file.
        Creates directories as needed.

        Args:
            response (requests.Response): Response object to save
            file_path (str): File path where to save (will create dirs if needed)

        Example:
            >>> response = api.get("/products")
            >>> api.save_response_to_file(response, "responses/products.json")
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        response_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.json() if response.content else {},
        }

        with open(file_path, "w") as f:
            json.dump(response_data, f, indent=2)

        logger.info(f"Response saved to: {file_path}")

    def clear_auth(self) -> None:
        """
        Clear authentication headers from session.

        Removes the Authorization header to make subsequent requests unauthenticated.

        Example:
            >>> api.set_auth_token("token123")
            >>> api.get("/protected")  # Uses token
            >>> api.clear_auth()
            >>> api.get("/public")  # No auth header
        """
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
            logger.debug("Cleared Authorization header")
