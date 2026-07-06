"""Exceptions."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import requests


class TestRailError(Exception):
    """Base Exception."""


class TestRailAPIError(TestRailError):
    """Base API Exception."""


class StatusCodeError(TestRailAPIError):
    """
    Raised when the API responds with a non-OK HTTP status code.

    The positional args keep the historical layout
    ``(status_code, reason, url, content)``, and the same values are also
    available as attributes, together with the full ``requests.Response``.
    """

    def __init__(
        self,
        status_code: int,
        reason: str,
        url: str,
        content: bytes,
        response: "requests.Response | None" = None,
    ) -> None:
        super().__init__(status_code, reason, url, content)
        self.status_code = status_code
        self.reason = reason
        self.url = url
        self.content = content
        self.response = response
