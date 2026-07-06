import json
import time
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from unittest import mock
from urllib.parse import parse_qs, urlparse

import pytest
import responses
from requests import Response, Session
from requests.exceptions import ConnectionError

from testrail_api import StatusCodeError
from testrail_api import TestRailAPI as TRApi
from testrail_api._category import _bulk_api_method
from testrail_api._exception import TestRailAPIError as TRApiError
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
    api = TRApi(*auth_data, raise_on_error=False)
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (429, {}, ""),
    )
    resp = api.cases.get_case(1)
    assert resp is None


def test_exc_raise(auth_data, mock, url):
    api = TRApi(*auth_data, raise_on_error=False)
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (400, {}, ""),
    )
    resp = api.cases.get_case(1)
    assert resp is None


def test_raise(auth_data, mock, url):
    api = TRApi(*auth_data)
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (400, {}, ""),
    )
    with pytest.raises(StatusCodeError):
        api.cases.get_case(1)


def test_custom_exception_fails(auth_data, mock, url):
    api = TRApi(*auth_data, raise_on_error=False, retry_exceptions=(CustomException,))
    mock.add_callback(responses.GET, url("get_case/1"), CustomExceptionRetry(fail=True))
    with pytest.raises(CustomException):
        api.cases.get_case(1)


def test_custom_exception_succeeds(auth_data, mock, url):
    api = TRApi(*auth_data, raise_on_error=False, retry_exceptions=(CustomException,))
    mock.add_callback(responses.GET, url("get_case/1"), CustomExceptionRetry(fail=False))
    response = api.cases.get_case(1)
    assert response.get("count") == 3


def test_custom_exception_fails_different_exception(auth_data, mock, url):
    api = TRApi(*auth_data, raise_on_error=False, retry_exceptions=(KeyboardInterrupt,))
    mock.add_callback(responses.GET, url("get_case/1"), CustomExceptionRetry(fail=True))
    with pytest.raises(CustomException):
        api.cases.get_case(1)


def test_no_response_raise():
    api = TRApi("https://asdadadsa.cd", "asd@asd.com", "asdasda")
    with pytest.raises(ConnectionError):
        api.cases.get_case(1)


def test_get_email():
    email = "asd@asd.com"
    api = TRApi("https://asdadadsa.cd", "asd@asd.com", "asdasda")
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
        TRApi("http://asdadadsa.cd", "asd@asd.com", "asdasda")


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


def test_categories_bound_to_own_instance():
    # Regression: categories used to be shared descriptors, so touching one API
    # instance rebound the category session of another. Each instance must keep
    # its own binding.
    api_a = TRApi("https://a.testrail.com/", "a@a.com", "password")
    api_b = TRApi("https://b.testrail.com/", "b@b.com", "password")

    runs_a = api_a.runs
    _ = api_b.runs.get_run  # touch the other instance's category

    assert runs_a.s is api_a
    assert api_b.runs.s is api_b
    assert api_a.runs is not api_b.runs


def test_category_is_cached_per_instance(auth_data):
    api = TRApi(*auth_data)
    assert api.runs is api.runs
    assert api.cases is api.cases


def test_categories_isolated_requests(mock):
    # Two clients on different hosts must send requests to their own base URL.
    api_a = TRApi("https://a.testrail.com/", "a@a.com", "password")
    api_b = TRApi("https://b.testrail.com/", "b@b.com", "password")
    mock.add_callback(
        responses.GET,
        "https://a.testrail.com/index.php?/api/v2/get_case/1",
        lambda _: (200, {}, json.dumps({"host": "a"})),
    )
    mock.add_callback(
        responses.GET,
        "https://b.testrail.com/index.php?/api/v2/get_case/1",
        lambda _: (200, {}, json.dumps({"host": "b"})),
    )
    runs_a = api_a.cases
    _ = api_b.cases.get_case(1)  # rebind attempt on the shared object (old bug)
    assert runs_a.get_case(1)["host"] == "a"


def test_context_manager_returns_self(auth_data):
    with TRApi(*auth_data) as api:
        assert isinstance(api, TRApi)


def test_context_manager_closes_session(auth_data):
    session = Session()
    with mock.patch.object(session, "close") as close_mock, TRApi(*auth_data, session=session):
        pass
    close_mock.assert_called_once()


def test_close_method(auth_data):
    session = Session()
    api = TRApi(*auth_data, session=session)
    with mock.patch.object(session, "close") as close_mock:
        api.close()
    close_mock.assert_called_once()


def test_request_return_none_with_zero_iterations():
    # Initialize session with 0 iterations so the request loop never runs
    api = TRApi("https://testrail.com", "user", "password", exc_iterations=0)

    # Call request - it should skip the loop and return None at line 238
    result = api.request("GET", "get_case/1")

    assert result is None


def test_exc_deprecated_but_works(auth_data, mock, url):
    with pytest.warns(DeprecationWarning, match="raise_on_error"):
        api = TRApi(*auth_data, exc=True)
    mock.add_callback(responses.GET, url("get_case/1"), lambda _: (400, {}, ""))
    assert api.cases.get_case(1) is None


def test_exc_false_deprecated_still_raises(auth_data, mock, url):
    with pytest.warns(DeprecationWarning, match="raise_on_error"):
        api = TRApi(*auth_data, exc=False)
    mock.add_callback(responses.GET, url("get_case/1"), lambda _: (400, {}, ""))
    with pytest.raises(StatusCodeError):
        api.cases.get_case(1)


def test_explicit_raise_on_error_wins_over_exc(auth_data, mock, url):
    with pytest.warns(DeprecationWarning):
        api = TRApi(*auth_data, exc=True, raise_on_error=True)
    mock.add_callback(responses.GET, url("get_case/1"), lambda _: (400, {}, ""))
    with pytest.raises(StatusCodeError):
        api.cases.get_case(1)


def test_unknown_constructor_kwarg_raises(auth_data):
    with pytest.raises(TypeError):
        TRApi(*auth_data, timout=60)  # typo of timeout must not be silently ignored


def test_status_code_error_attributes(auth_data, mock, url):
    api = TRApi(*auth_data)
    mock.add_callback(responses.GET, url("get_case/1"), lambda _: (400, {}, "error body"))
    with pytest.raises(StatusCodeError) as exc_info:
        api.cases.get_case(1)
    e = exc_info.value
    assert e.status_code == 400
    assert e.content == b"error body"
    assert "get_case/1" in e.url
    assert isinstance(e.response, Response)
    # historical positional args layout is preserved
    assert e.args == (e.status_code, e.reason, e.url, e.content)


def test_get_params_are_not_mutated(api, mock, url):
    mock.add_callback(responses.GET, url("get_cases/1"), lambda _: (200, {}, json.dumps({})))
    created_after = datetime(2026, 1, 1, tzinfo=timezone.utc)
    params = {"created_by": [1, 2], "is_completed": True, "created_after": created_after}
    api.get("get_cases/1", params=params)
    assert params == {"created_by": [1, 2], "is_completed": True, "created_after": created_after}


def test_get_params_conversion(api, mock, url):
    def callback(request) -> tuple[int, dict, str]:
        query = parse_qs(urlparse(request.url).query)
        assert query["created_by"] == ["1,2"]
        assert query["is_completed"] == ["1"]
        assert query["type_id"] == ["1,2,3"]  # sets are sent in a deterministic order
        return 200, {}, json.dumps({})

    mock.add_callback(responses.GET, url("get_cases/1"), callback)
    api.get("get_cases/1", params={"created_by": (1, 2), "is_completed": True, "type_id": {3, 1, 2}})


def test_post_nested_datetime_converted(api, mock, url):
    when = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def callback(request) -> tuple[int, dict, str]:
        body = json.loads(request.body)
        assert body["results"][0]["custom_finished_on"] == round(when.timestamp())
        return 200, {}, json.dumps([])

    mock.add_callback(responses.POST, url("add_results/1"), callback)
    results = [{"test_id": 1, "status_id": 1, "custom_finished_on": when}]
    api.results.add_results(1, results)
    # the caller's nested structure must stay untouched
    assert results[0]["custom_finished_on"] is when


def test_rate_limit_retry_after_http_date(api, mock, url):
    http_date = format_datetime(datetime.now(timezone.utc) - timedelta(seconds=10), usegmt=True)
    calls = {"count": 0}

    def callback(_) -> tuple[int, dict, str]:
        calls["count"] += 1
        if calls["count"] == 1:
            return 429, {"retry-after": http_date}, ""
        return 200, {}, json.dumps({"id": 1})

    mock.add_callback(responses.GET, url("get_case/1"), callback)
    start = time.monotonic()
    assert api.cases.get_case(1)["id"] == 1
    assert calls["count"] == 2
    assert time.monotonic() - start < 3  # past date clamps the delay to zero


def test_rate_limit_retry_after_seconds(api, mock, url):
    calls = {"count": 0}

    def callback(_) -> tuple[int, dict, str]:
        calls["count"] += 1
        if calls["count"] == 1:
            return 429, {"retry-after": "0"}, ""
        return 200, {}, json.dumps({"id": 1})

    mock.add_callback(responses.GET, url("get_case/1"), callback)
    assert api.cases.get_case(1)["id"] == 1
    assert calls["count"] == 2


def test_bulk_rejects_limit_and_offset(api):
    with pytest.raises(TypeError, match="managed automatically"):
        api.cases.get_cases_bulk(1, limit=10)
    with pytest.raises(TypeError, match="managed automatically"):
        api.cases.get_cases_bulk(1, offset=10)


def test_bulk_non_paginated_response():
    mock_func = mock.Mock(return_value=[{"id": 1}])
    with pytest.raises(TRApiError, match="paginated"):
        _bulk_api_method(mock_func, "cases")


def test_bulk_missing_key():
    mock_func = mock.Mock(return_value={"offset": 0, "limit": 250, "size": 0})
    with pytest.raises(TRApiError, match="'cases'"):
        _bulk_api_method(mock_func, "cases")


def test_bulk_null_page():
    mock_func = mock.Mock(return_value={"offset": 0, "limit": 250, "size": 0, "cases": None})
    assert _bulk_api_method(mock_func, "cases") == []


def test_get_attachment_error_uses_custom_handler(auth_data, mock, url, tmp_path):
    api = TRApi(*auth_data, response_handler=lambda _: "custom error")
    mock.add_callback(responses.GET, url("get_attachment/1"), lambda _: (400, {}, ""))
    assert api.attachments.get_attachment(1, tmp_path / "file.bin") == "custom error"
    assert not (tmp_path / "file.bin").exists()


def test_sensitive_headers_redacted_in_log(auth_data, caplog):
    with caplog.at_level("INFO", logger="testrail_api"):
        TRApi(*auth_data, headers={"Authorization": "top-secret", "X-Custom": "visible"})
    assert "top-secret" not in caplog.text
    assert "***" in caplog.text
    assert "visible" in caplog.text
