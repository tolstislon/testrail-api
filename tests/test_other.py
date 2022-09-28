from functools import partial
import json
import time

import pytest
import responses
from requests.exceptions import ConnectionError

from testrail_api import StatusCodeError, TestRailAPI as TRApi
from testrail_api._exception import TestRailError as TRError  # noqa


class RateLimit:

    def __init__(self):
        self.last = 0
        self.count = 0

    def rate(self, r):
        self.count += 1
        now = time.time()
        if self.last == 0 or now - self.last < 3:
            self.last = now
            return 429, {}, ''
        else:
            return 200, {}, json.dumps({'count': self.count})


class CustomException(Exception):
    pass


class CustomExceptionRetry:

    def __init__(self, exception=CustomException, fail=False):
        self.count = 0
        self.exception = exception
        self.fail = fail

    def raises(self, *args, **kwargs):
        self.count += 1
        if self.count < 3:
            print(self.count)
            raise self.exception("fail")
        elif self.fail:
            raise self.exception("fail")
        else:
            return 200, {}, json.dumps({'count': self.count})


def test_rate_limit(api, mock, host):
    limit = RateLimit()
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        limit.rate,
    )
    resp = api.cases.get_case(1)
    assert resp['count'] == 2


def test_raise_rate_limit(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        lambda x: (429, {}, ''),
    )
    with pytest.raises(StatusCodeError):
        api.cases.get_case(1)


def test_exc_raise_rate_limit(auth_data, mock, host):
    api = TRApi(*auth_data, exc=True)
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        lambda x: (429, {}, ''),
    )
    resp = api.cases.get_case(1)
    assert resp is None


def test_exc_raise(auth_data, mock, host):
    api = TRApi(*auth_data, exc=True)
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        lambda x: (400, {}, ''),
    )
    resp = api.cases.get_case(1)
    assert resp is None


def test_raise(auth_data, mock, host):
    api = TRApi(*auth_data, exc=False)
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        lambda x: (400, {}, ''),
    )
    with pytest.raises(StatusCodeError):
        api.cases.get_case(1)


def test_custom_exception_fails(auth_data, mock, host):
    retry = CustomExceptionRetry(fail=True)
    api = TRApi(*auth_data, exc=True, retry_exceptions=(CustomException,))
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        retry.raises,
    )
    with pytest.raises(CustomException):
        api.cases.get_case(1)

def test_custom_exception_succeeds(auth_data, mock, host):
    retry = CustomExceptionRetry(fail=False)
    api = TRApi(*auth_data, exc=True, retry_exceptions=(CustomException,))
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        retry.raises,
    )
    response = api.cases.get_case(1)
    assert response.get('count') is 3

def test_custom_exception_fails_different_exception(auth_data, mock, host):
    retry = CustomExceptionRetry(fail=True)
    api = TRApi(*auth_data, exc=True, retry_exceptions=(KeyboardInterrupt,))
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        retry.raises,
    )
    with pytest.raises(CustomException):
        api.cases.get_case(1)

def test_no_response_raise():
    api = TRApi('https://asdadadsa.cd', 'asd@asd.com', 'asdasda', exc=False)
    with pytest.raises(ConnectionError):
        api.cases.get_case(1)


def test_get_email():
    email = 'asd@asd.com'
    api = TRApi('https://asdadadsa.cd', 'asd@asd.com', 'asdasda', exc=False)
    assert api.user_email == email


@pytest.mark.parametrize('field', ('url', 'email', 'password'))
def test_raise_no_arg(field):
    data = {'url': 'https://asdadadsa.cd', 'email': 'asd@asd.com', 'password': 'asdasda'}
    del data[field]
    with pytest.raises(TRError):
        TRApi(**data)


def test_environment_variables(environ, mock, host):
    api = TRApi()
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        lambda x: (200, {}, json.dumps({'id': 1})),
    )
    resp = api.cases.get_case(1)
    assert resp['id'] == 1


def test_http_warn():
    with pytest.warns(UserWarning):
        TRApi('http://asdadadsa.cd', 'asd@asd.com', 'asdasda', exc=False)


@pytest.mark.filterwarnings("error")
def test_http_no_warn():
    TRApi('http://asdadadsa.cd', 'asd@asd.com', 'asdasda', warn_ignore=True)
