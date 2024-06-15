"""Base session"""

import logging
import time
import warnings
from datetime import datetime
from json.decoder import JSONDecodeError
from os import environ
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

import requests

from . import __version__
from ._enums import METHODS
from ._exception import StatusCodeError, TestRailError


logger = logging.getLogger(__package__)

RATE_LIMIT_STATUS_CODE = 429


class Environ:
    URL: str = "TESTRAIL_URL"
    EMAIL: str = "TESTRAIL_EMAIL"
    PASSWORD: str = "TESTRAIL_PASSWORD"


class Session:
    """Base Session"""

    _user_agent = f"Python TestRail API v: {__version__}"

    def __init__(
        self,
        url: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        *,
        exc: bool = False,
        rate_limit: bool = True,
        warn_ignore: bool = False,
        retry_exceptions: Tuple[Type[BaseException], ...] = (),
        response_handler: Callable[[requests.Response], Any] = None,
        session: Optional[requests.Session] = None,
        **kwargs,
    ) -> None:
        """
        :param url:
            TestRail address
        :param email:
            Email for the account on the TestRail
        :param password:
            Password for the account on the TestRail or token
        :param session:
            Given session will be used instead of new one
        :param exc:
            Catching exceptions
        :param rate_limit:
            Check the response header for the rate limit and retry the request
        :param warn_ignore:
            Ignore warning when not using HTTPS
        :param retry_exceptions:
            Set of exceptions to retry the request
        :param response_hook:
            Override default response handling
        :param kwargs:
            :key timeout: int (default: 30)
                How many seconds to wait for the server to send data
            :key verify: bool (default: True)
                Controls whether we verify the server's certificate
            :key headers: dict
                Dictionary of HTTP Headers to send
            :key retry: int (default 3)
                Delay in receiving code 429
            :key exc_iterations: int (default 3)
        """
        _url = self.__get_url(url=url, warn_ignore=warn_ignore)
        _email = self.__get_email(email=email)
        _password = self.__get_password(password=password)
        self.__base_url = f"{_url}/index.php?/api/v2/"
        self.__timeout = kwargs.get("timeout", 30)
        self.__session = session or requests.Session()
        self.__session.headers["User-Agent"] = self._user_agent
        self.__session.headers.update(kwargs.get("headers", {}))
        self.__session.verify = kwargs.get("verify", True)
        self.__retry = kwargs.get("retry", 3)
        self.__user_email = _email
        self.__session.auth = (self.__user_email, _password)
        self.__exc = exc
        self.__retry_exceptions = (KeyError, *retry_exceptions)
        self.__exc_iterations = kwargs.get("exc_iterations", 3)
        self.__response_handler = response_handler or self.__default_response_handler
        self._rate_limit = rate_limit
        logger.info(
            "Create Session{url: %s, user: %s, timeout: %s, headers: %s, verify: "
            "%s, exception: %s, exc_iterations: %s, retry: %s}",
            url,
            self.__user_email,
            self.__timeout,
            self.__session.headers,
            self.__session.verify,
            self.__exc,
            self.__exc_iterations,
            self.__retry,
        )

    @property
    def user_email(self) -> str:
        """Get user email"""
        return self.__user_email

    @staticmethod
    def __get_url(url: str, warn_ignore: bool) -> str:
        """Reading URL"""
        _url = url or environ.get(Environ.URL)
        if not _url:
            raise TestRailError(f"Url is not set. Use argument url or env {Environ.URL}")
        _url = _url.rstrip("/")
        if _url.startswith("http://") and not warn_ignore:
            warnings.warn("Using HTTP and not HTTPS may cause writeable API requests to return 404 errors")
        return _url

    @staticmethod
    def __get_email(email: Optional[str]) -> str:
        """Reading email"""
        _email = email or environ.get(Environ.EMAIL)
        if not _email:
            raise TestRailError(f"Email is not set. Use argument email or env {Environ.EMAIL}")
        return _email

    @staticmethod
    def __get_password(password: str) -> str:
        """Reading password"""
        _password = password or environ.get(Environ.PASSWORD)
        if not _password:
            raise TestRailError(f"Password is not set. Use argument password or env {Environ.PASSWORD}")
        return _password

    def __default_response_handler(self, response: requests.Response):
        """Default response handler. Deserialization json or return None"""
        if not response.ok:
            logger.error(
                "Code: %s, reason: %s url: %s, content: %s",
                response.status_code,
                response.reason,
                response.url,
                response.content,
            )
            if not self.__exc:
                raise StatusCodeError(
                    response.status_code,
                    response.reason,
                    response.url,
                    response.content,
                )
        logger.debug("Response body: %s", response.text)
        try:
            return response.json()
        except (JSONDecodeError, ValueError):
            return response.text or None

    @staticmethod
    def __get_converter(params: dict) -> None:
        """Converting GET parameters"""
        for key, value in params.items():
            if isinstance(value, (list, tuple, set)):
                # Converting a list to a string '1,2,3'
                params[key] = ",".join(str(i) for i in value)
            elif isinstance(value, bool):
                # Converting a boolean value to integer
                params[key] = int(value)
            elif isinstance(value, datetime):
                # Converting a datetime value to integer (UNIX timestamp)
                params[key] = round(value.timestamp())

    @staticmethod
    def __post_converter(json: dict) -> None:
        """Converting POST parameters"""
        for key, value in json.items():
            if isinstance(value, datetime):
                # Converting a datetime value to integer (UNIX timestamp)
                json[key] = round(value.timestamp())

    def get(self, endpoint: str, params: Optional[Dict[Any, Any]] = None):
        """GET method"""
        return self.request(
            method=METHODS.GET,
            endpoint=endpoint,
            params=params or {},
        )

    def post(
        self,
        endpoint: str,
        params: Optional[Dict[Any, Any]] = None,
        json: Optional[Dict[Any, Any]] = None,
    ):
        """POST method"""
        return self.request(
            method=METHODS.POST,
            endpoint=endpoint,
            params=params or {},
            json=json or {},
        )

    def request(self, method: METHODS, endpoint: str, raw: bool = False, **kwargs):
        """Base request method"""
        url = f"{self.__base_url}{endpoint}"
        if not endpoint.startswith("add_attachment"):
            headers = kwargs.setdefault("headers", {})
            headers.update({"Content-Type": "application/json"})

        self.__get_converter(kwargs.get("params", {}))
        self.__post_converter(kwargs.get("json", {}))

        for count in range(self.__exc_iterations):
            try:
                response = self.__session.request(method=str(method.value), url=url, timeout=self.__timeout, **kwargs)
            except self.__retry_exceptions as exc:
                if count < self.__exc_iterations - 1:
                    logger.warning("%s, retrying %s/%s", exc, count + 1, self.__exc_iterations)
                    continue
                else:
                    raise
            except Exception as err:
                logger.error("%s", err, exc_info=True)
                raise
            if (
                self._rate_limit
                and response.status_code == RATE_LIMIT_STATUS_CODE
                and count < self.__exc_iterations - 1
            ):
                time.sleep(int(response.headers.get("retry-after", self.__retry)))
                continue
            logger.debug("Response header: %s", response.headers)
            return response if raw else self.__response_handler(response)

    @staticmethod
    def _path(path: Union[Path, str]) -> Path:
        return path if isinstance(path, Path) else Path(path)

    def attachment_request(self, method: METHODS, src: str, file: Union[Path, str], **kwargs):
        """Send attach"""
        file = self._path(file)
        with file.open("rb") as attachment:
            return self.request(method, src, files={"attachment": attachment}, **kwargs)

    def get_attachment(self, method: METHODS, src: str, file: Union[Path, str], **kwargs) -> Path:
        """Downloads attach"""
        file = self._path(file)
        response = self.request(method, src, raw=True, **kwargs)
        if response.ok:
            with file.open("wb") as attachment:
                attachment.write(response.content)
            return file
        return self.__default_response_handler(response)
