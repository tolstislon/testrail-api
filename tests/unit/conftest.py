import os
from pathlib import Path

import pytest
import responses

from testrail_api import TestRailAPI

BASE_HOST = 'https://example.testrail.com/index.php?/api/v2/'


class CallbackResponse(responses.CallbackResponse):

    def _url_matches(self, url: str, other, match_querystring=False):
        base_url = url.replace(BASE_HOST, '')
        other = other.replace(BASE_HOST, '')
        base_other = other.split('&', 1)[0]
        f = base_url == base_other
        return f


class RequestsMock(responses.RequestsMock):

    def add_callback(self, method, url, callback, match_querystring=False, content_type="text/plain"):
        self._matches.append(
            CallbackResponse(
                url=url,
                method=method,
                callback=callback,
                content_type=content_type,
                match_querystring=match_querystring,
            )
        )


@pytest.fixture(scope='session')
def host():
    yield 'https://example.testrail.com/'


@pytest.fixture(scope='session')
def base_path():
    path = Path(__file__).absolute().parent
    yield str(path)


@pytest.fixture(scope='session')
def auth_data(host):
    yield host, 'example@mail.com', 'password'


@pytest.fixture
def mock():
    with RequestsMock() as resp:
        yield resp


@pytest.fixture
def api(auth_data):
    api = TestRailAPI(*auth_data)
    yield api


@pytest.fixture
def environ(auth_data):
    os.environ['TESTRAIL_URL'] = auth_data[0]
    os.environ['TESTRAIL_EMAIL'] = auth_data[1]
    os.environ['TESTRAIL_PASSWORD'] = auth_data[2]
    yield
    del os.environ['TESTRAIL_URL']
    del os.environ['TESTRAIL_EMAIL']
    del os.environ['TESTRAIL_PASSWORD']
