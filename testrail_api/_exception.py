"""Exceptions."""

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    import requests


class TestRailError(Exception):
    """Base Exception."""


class TestRailAPIError(TestRailError):
    """Base API Exception."""


class StatusCodeError(TestRailAPIError):
    """
    Raised when the API responds with a non-OK HTTP status code.

    Common status codes raise a dedicated subclass (:class:`AuthError`,
    :class:`NotFoundError`, :class:`RateLimitError`, :class:`ServerError`),
    so ``except StatusCodeError`` keeps catching all of them.

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


class AuthError(StatusCodeError):
    """Raised for HTTP 401/403 responses: invalid credentials or insufficient permissions."""


class NotFoundError(StatusCodeError):
    """Raised for HTTP 404 responses: unknown endpoint or entity."""


class RateLimitError(StatusCodeError):
    """Raised for HTTP 429 responses, once rate-limit retries are exhausted."""


class ServerError(StatusCodeError):
    """Raised for HTTP 5xx responses."""


_SERVER_ERROR_FLOOR: Final[int] = 500
_STATUS_EXCEPTIONS: Final[dict[int, type[StatusCodeError]]] = {
    401: AuthError,
    403: AuthError,
    404: NotFoundError,
    429: RateLimitError,
}


def status_error_class(status_code: int) -> type[StatusCodeError]:
    """Pick the :class:`StatusCodeError` subclass matching an HTTP status code."""
    if status_code >= _SERVER_ERROR_FLOOR:
        return ServerError
    return _STATUS_EXCEPTIONS.get(status_code, StatusCodeError)
