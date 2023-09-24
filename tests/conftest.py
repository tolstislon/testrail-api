import os
from pathlib import Path

import pytest
import responses


try:
    from responses import FalseBool


    false_bool = FalseBool()
except ImportError:
    false_bool = False

from testrail_api import TestRailAPI


BASE_HOST = 'https://example.testrail.com/index.php?/api/v2/'


class CallbackResponse(responses.CallbackResponse):

    def _url_matches(self, url: str, other, match_querystring=false_bool):
        base_url = url.replace(BASE_HOST, '')
        other = other.replace(BASE_HOST, '')
        base_other = other.split('&', 1)[0]
        f = base_url == base_other
        return f


class RequestsMock(responses.RequestsMock):

    def add_callback(self, method, url, callback, match_querystring=false_bool,
                     content_type="text/plain", match=()):
        self._registry.add(
            CallbackResponse(
                url=url,
                method=method,
                callback=callback,
                content_type=content_type,
                match_querystring=match_querystring,
                match=match
            )
        )


@pytest.fixture(scope='session')
def host():
    return 'https://example.testrail.com/'


@pytest.fixture(scope='session')
def url(host):
    def _wrap(endpoint: str) -> str:
        return f'{host}index.php?/api/v2/{endpoint}'

    yield _wrap


@pytest.fixture(scope='session')
def base_path():
    path = Path(__file__).absolute().parent
    return str(path)


@pytest.fixture(scope='session')
def auth_data(host):
    return host, 'example@mail.com', 'password'


@pytest.fixture
def mock():
    with RequestsMock() as resp:
        yield resp


@pytest.fixture
def api(auth_data):
    return TestRailAPI(*auth_data)


@pytest.fixture
def environ(auth_data):
    os.environ['TESTRAIL_URL'] = auth_data[0]
    os.environ['TESTRAIL_EMAIL'] = auth_data[1]
    os.environ['TESTRAIL_PASSWORD'] = auth_data[2]
    yield
    del os.environ['TESTRAIL_URL']
    del os.environ['TESTRAIL_EMAIL']
    del os.environ['TESTRAIL_PASSWORD']
