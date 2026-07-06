"""Base session."""

import logging
import time
import warnings
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from json.decoder import JSONDecodeError
from os import environ
from pathlib import Path
from types import TracebackType
from typing import Any, Final, TypeVar

import requests

from . import __version__
from ._enums import METHODS
from ._exception import StatusCodeError, TestRailError

logger = logging.getLogger(__package__)

RATE_LIMIT_STATUS_CODE: Final[int] = 429
MAX_RATE_LIMIT_DELAY: Final[float] = 300.0
DOWNLOAD_CHUNK_SIZE: Final[int] = 2**20

_SENSITIVE_HEADERS: Final[frozenset[str]] = frozenset(
    {"authorization", "proxy-authorization", "cookie", "set-cookie", "x-api-key"},
)

_S = TypeVar("_S", bound="Session")


class Environ:
    URL: str = "TESTRAIL_URL"
    EMAIL: str = "TESTRAIL_EMAIL"
    PASSWORD: str = "TESTRAIL_PASSWORD"  # noqa: S105


class Session:
    """Base Session."""

    _user_agent = f"Python TestRail API v: {__version__}"

    def __init__(  # noqa: PLR0913
        self,
        url: str | None = None,
        email: str | None = None,
        password: str | None = None,
        *,
        timeout: float | tuple[float, float] = 30,
        verify: bool | str = True,
        headers: dict[str, str] | None = None,
        retry: float = 3,
        exc_iterations: int = 3,
        raise_on_error: bool | None = None,
        exc: bool | None = None,
        rate_limit: bool = True,
        warn_ignore: bool = False,
        retry_exceptions: tuple[type[BaseException], ...] = (),
        response_handler: Callable[[requests.Response], Any] | None = None,
        session: requests.Session | None = None,
    ) -> None:
        """
        Session constructor.

        :param url:
            TestRail address.
        :param email:
            Email for the account on the TestRail.
        :param password:
            Password for the account on the TestRail or token.
        :param timeout:
            How many seconds to wait for the server to send data (default: 30).
            May be a ``(connect, read)`` tuple.
        :param verify:
            Controls whether we verify the server's certificate (default: True).
        :param headers:
            Dictionary of HTTP headers to send with every request.
        :param retry:
            Delay in seconds between retries on HTTP 429 when the response
            has no valid retry-after header (default: 3).
        :param exc_iterations:
            Number of attempts for rate-limit and ``retry_exceptions`` retries (default: 3).
        :param raise_on_error:
            Raise :class:`StatusCodeError` for non-OK responses (default: True).
        :param exc:
            Deprecated, use ``raise_on_error`` (note the inverted meaning:
            ``exc=True`` matches ``raise_on_error=False``).
        :param rate_limit:
            Check the response for HTTP 429 and retry the request.
        :param warn_ignore:
            Ignore warning when not using HTTPS.
        :param retry_exceptions:
            Set of exceptions to retry the request.
        :param response_handler:
            Override default response handling.
        :param session:
            A Given session will be used instead of new one.
        """
        _url = self.__require(url, Environ.URL, "Url").rstrip("/")
        if _url.startswith("http://") and not warn_ignore:
            warnings.warn(
                "Using HTTP and not HTTPS may cause writeable API requests to return 404 errors", stacklevel=2
            )
        _email = self.__require(email, Environ.EMAIL, "Email")
        _password = self.__require(password, Environ.PASSWORD, "Password")
        self.__base_url = f"{_url}/index.php?/api/v2/"
        self.__timeout = timeout
        self.__session = session or requests.Session()
        self.__session.headers["User-Agent"] = self._user_agent
        self.__session.headers.update(headers or {})
        self.__session.verify = verify
        self.__retry = retry
        self.__user_email = _email
        self.__session.auth = (self.__user_email, _password)
        if exc is not None:
            warnings.warn(
                "The 'exc' argument is deprecated, use 'raise_on_error' instead "
                "(note the inverted meaning: exc=True matches raise_on_error=False)",
                DeprecationWarning,
                stacklevel=2,
            )
        if raise_on_error is None:
            raise_on_error = True if exc is None else not exc
        self.__raise_on_error = raise_on_error
        self.__retry_exceptions = tuple(retry_exceptions)
        self.__exc_iterations = exc_iterations
        self.__response_handler = response_handler or self.__default_response_handler
        self._rate_limit = rate_limit
        logger.info(
            "Create Session{url: %s, user: %s, timeout: %s, headers: %s, verify: "
            "%s, raise_on_error: %s, exc_iterations: %s, retry: %s}",
            _url,
            self.__user_email,
            self.__timeout,
            self._redact_headers(self.__session.headers),
            self.__session.verify,
            self.__raise_on_error,
            self.__exc_iterations,
            self.__retry,
        )

    @property
    def user_email(self) -> str:
        """Get user email."""
        return self.__user_email

    def close(self) -> None:
        """Close the underlying HTTP session and release pooled connections."""
        self.__session.close()

    def __enter__(self: _S) -> _S:
        """Enter the runtime context and return the session."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Close the session when leaving the runtime context."""
        self.close()

    @staticmethod
    def __require(value: str | None, env_var: str, name: str) -> str:
        """Read a required setting from the argument or the environment variable."""
        if not (result := value or environ.get(env_var)):
            raise TestRailError(f"{name} is not set. Use argument {name.lower()} or env {env_var}")
        return result

    @staticmethod
    def _redact_headers(headers: Mapping[str, Any]) -> dict[str, Any]:
        """Replace values of sensitive headers so they can be logged safely."""
        return {key: "***" if key.lower() in _SENSITIVE_HEADERS else value for key, value in headers.items()}

    def __default_response_handler(self, response: requests.Response) -> Any:
        """Deserialization json or return None."""
        if not response.ok:
            logger.error(
                "Code: %s, reason: %s url: %s, content: %s",
                response.status_code,
                response.reason,
                response.url,
                response.content,
            )
            if self.__raise_on_error:
                raise StatusCodeError(
                    response.status_code,
                    response.reason,
                    response.url,
                    response.content,
                    response=response,
                )
        logger.debug("Response body: %s", response.text)
        try:
            return response.json()
        except (JSONDecodeError, ValueError):
            return response.text or None

    @staticmethod
    def __get_converter(params: dict) -> dict:
        """Convert GET parameters, returning a new dict."""
        converted = {}
        for key, value in params.items():
            if isinstance(value, bool):
                # Converting a boolean value to integer
                converted[key] = int(value)
            elif isinstance(value, (list, tuple, set)):
                # Converting a collection to a string '1,2,3' (sets are sorted for determinism)
                items = sorted(value, key=str) if isinstance(value, set) else value
                converted[key] = ",".join(str(i) for i in items)
            elif isinstance(value, datetime):
                # Converting a datetime value to integer (UNIX timestamp)
                converted[key] = round(value.timestamp())
            else:
                converted[key] = value
        return converted

    @classmethod
    def __post_converter(cls, json: Any) -> Any:
        """Convert POST parameters recursively, returning a new structure."""
        if isinstance(json, datetime):
            # Converting a datetime value to integer (UNIX timestamp)
            return round(json.timestamp())
        if isinstance(json, dict):
            return {key: cls.__post_converter(value) for key, value in json.items()}
        if isinstance(json, (list, tuple)):
            return [cls.__post_converter(value) for value in json]
        return json

    @staticmethod
    def _parse_retry_after(value: str) -> float | None:
        """Parse a retry-after header: either a number of seconds or an HTTP-date."""
        value = value.strip()
        if not value:
            return None
        try:
            return float(value)
        except ValueError:
            pass
        try:
            date = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
        return (date - datetime.now(timezone.utc)).total_seconds()

    def get(self, endpoint: str, params: dict[Any, Any] | None = None) -> Any:
        """GET method."""
        return self.request(
            method=METHODS.GET,
            endpoint=endpoint,
            params=params or {},
        )

    def post(
        self,
        endpoint: str,
        params: dict[Any, Any] | None = None,
        json: dict[Any, Any] | None = None,
    ) -> Any:
        """POST method."""
        return self.request(
            method=METHODS.POST,
            endpoint=endpoint,
            params=params or {},
            json=json or {},
        )

    def request(self, method: METHODS, endpoint: str, *, raw: bool = False, **kwargs) -> Any:
        """Send request method."""
        url = f"{self.__base_url}{endpoint}"
        if not endpoint.startswith(("add_attachment", "add_bdd")):
            headers = kwargs.setdefault("headers", {})
            headers.update({"Content-Type": "application/json"})

        if "params" in kwargs:
            kwargs["params"] = self.__get_converter(kwargs["params"])
        if "json" in kwargs:
            kwargs["json"] = self.__post_converter(kwargs["json"])

        for count in range(self.__exc_iterations):
            try:
                response = self.__session.request(method=str(method.value), url=url, timeout=self.__timeout, **kwargs)
            except self.__retry_exceptions as exc:
                if count < self.__exc_iterations - 1:
                    logger.warning("%s, retrying %s/%s", exc, count + 1, self.__exc_iterations)
                    continue
                raise
            except Exception:
                logger.exception("Request error")
                raise
            if (
                self._rate_limit
                and response.status_code == RATE_LIMIT_STATUS_CODE
                and count < self.__exc_iterations - 1
            ):
                retry_after = self._parse_retry_after(response.headers.get("retry-after", ""))
                delay = self.__retry if retry_after is None else retry_after
                delay = min(max(delay, 0.0), MAX_RATE_LIMIT_DELAY)
                logger.warning(
                    "Rate limit (429) on %s, sleeping %s sec before retry %s/%s",
                    url,
                    delay,
                    count + 1,
                    self.__exc_iterations,
                )
                time.sleep(delay)
                continue
            logger.debug("Response header: %s", response.headers)
            return response if raw else self.__response_handler(response)
        return None

    @staticmethod
    def _path(path: Path | str) -> Path:
        return path if isinstance(path, Path) else Path(path)

    def attachment_request(self, method: METHODS, src: str, file: Path | str, **kwargs) -> dict:
        """Send attach."""
        file = self._path(file)
        with file.open("rb") as attachment:
            return self.request(method, src, files={"attachment": attachment}, **kwargs)

    def get_attachment(self, method: METHODS, src: str, file: Path | str, **kwargs) -> Path:
        """Download attach."""
        file = self._path(file)
        response = self.request(method, src, raw=True, stream=True, **kwargs)
        try:
            if response.ok:
                with file.open("wb") as attachment:
                    for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                        attachment.write(chunk)
                return file
            return self.__response_handler(response)
        finally:
            response.close()
