import json
import time
from unittest import mock

import pytest
import responses
from requests import Session
from requests.exceptions import ConnectionError

from testrail_api import StatusCodeError
from testrail_api import TestRailAPI as TRApi
from testrail_api._category import _bulk_api_method
from testrail_api._exception import TestRailError as TRError


class RateLimit:
    """Rate limit test class."""

    def __init__(self):
        self.last = 0
        self.count = 0

    def __call__(self, r) -> tuple[int, dict, str]:
        self.count += 1
        now = time.time()
        if self.last == 0 or now - self.last < 3:
            self.last = now
            return 429, {}, ""
        return 200, {}, json.dumps({"count": self.count})


class CustomException(Exception):
    """Base custom exception."""


class CustomExceptionRetry:
    """Exception retry."""

    def __init__(self, exception=CustomException, *, fail=False) -> None:
        self.count = 0
        self.exception = exception
        self.fail = fail

    def __call__(self, *args, **kwargs) -> tuple[int, dict, str]:
        self.count += 1
        if self.count < 3 or self.fail:
            raise self.exception("fail")
        return 200, {}, json.dumps({"count": self.count})


class CustomSession(Session):
    """Custom session object."""

    def request(*args, **kwargs) -> None:
        """Session request."""
        raise ValueError("CustomSession")


def test_rate_limit(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        RateLimit(),
    )
    resp = api.cases.get_case(1)
    assert resp["count"] == 2


def test_raise_rate_limit(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (429, {}, ""),
    )
    with pytest.raises(StatusCodeError):
        api.cases.get_case(1)


def test_exc_raise_rate_limit(auth_data, mock, url):
    api = TRApi(*auth_data, exc=True)
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (429, {}, ""),
    )
    resp = api.cases.get_case(1)
    assert resp is None


def test_exc_raise(auth_data, mock, url):
    api = TRApi(*auth_data, exc=True)
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (400, {}, ""),
    )
    resp = api.cases.get_case(1)
    assert resp is None


def test_raise(auth_data, mock, url):
    api = TRApi(*auth_data, exc=False)
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (400, {}, ""),
    )
    with pytest.raises(StatusCodeError):
        api.cases.get_case(1)


def test_custom_exception_fails(auth_data, mock, url):
    api = TRApi(*auth_data, exc=True, retry_exceptions=(CustomException,))
    mock.add_callback(responses.GET, url("get_case/1"), CustomExceptionRetry(fail=True))
    with pytest.raises(CustomException):
        api.cases.get_case(1)


def test_custom_exception_succeeds(auth_data, mock, url):
    api = TRApi(*auth_data, exc=True, retry_exceptions=(CustomException,))
    mock.add_callback(responses.GET, url("get_case/1"), CustomExceptionRetry(fail=False))
    response = api.cases.get_case(1)
    assert response.get("count") == 3


def test_custom_exception_fails_different_exception(auth_data, mock, url):
    api = TRApi(*auth_data, exc=True, retry_exceptions=(KeyboardInterrupt,))
    mock.add_callback(responses.GET, url("get_case/1"), CustomExceptionRetry(fail=True))
    with pytest.raises(CustomException):
        api.cases.get_case(1)


def test_no_response_raise():
    api = TRApi("https://asdadadsa.cd", "asd@asd.com", "asdasda", exc=False)
    with pytest.raises(ConnectionError):
        api.cases.get_case(1)


def test_get_email():
    email = "asd@asd.com"
    api = TRApi("https://asdadadsa.cd", "asd@asd.com", "asdasda", exc=False)
    assert api.user_email == email


@pytest.mark.parametrize("field", ("url", "email", "password"))
def test_raise_no_arg(field):
    data = {"url": "https://asdadadsa.cd", "email": "asd@asd.com", "password": "asdasda"}
    del data[field]
    with pytest.raises(TRError):
        TRApi(**data)


@pytest.mark.usefixtures("environ")
def test_environment_variables(mock, url):
    api = TRApi()
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (200, {}, json.dumps({"id": 1})),
    )
    resp = api.cases.get_case(1)
    assert resp["id"] == 1


def test_http_warn():
    with pytest.warns(UserWarning):
        TRApi("http://asdadadsa.cd", "asd@asd.com", "asdasda", exc=False)


@pytest.mark.filterwarnings("error")
def test_http_no_warn():
    TRApi("http://asdadadsa.cd", "asd@asd.com", "asdasda", warn_ignore=True)


def test_response_handler(auth_data, mock, url):
    def hook(_) -> str:
        return "my hook response"

    api = TRApi(*auth_data, response_handler=hook)
    mock.add_callback(responses.GET, url("get_case/1"), lambda _: (200, {}, json.dumps({"a": 1, "b": 2})))
    response = api.cases.get_case(1)
    assert response == "my hook response"


def test_bulk_endpoint_helper():
    mock_func = mock.Mock()
    mock_func.side_effect = [
        {"offset": 0, "limit": 250, "size": 250, "data": [{"id": _} for _ in range(250)]},
        {"offset": 250, "limit": 250, "size": 1, "data": [{"id": 101}]},
    ]
    resp = _bulk_api_method(mock_func, "data")
    assert len(resp) == 251
    assert all("id" in _ for _ in resp)


def test_add_custom_session(auth_data):
    api = TRApi(*auth_data, session=CustomSession())
    with pytest.raises(ValueError, match="CustomSession"):
        api.users.get_users()
