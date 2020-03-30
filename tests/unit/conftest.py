import pytest
import responses

from testrail_api import TestRailAPI


@pytest.fixture(scope='session')
def host():
    yield 'https://example.testrail.com/'


@pytest.fixture
def mock():
    with responses.RequestsMock() as resp:
        yield resp


@pytest.fixture
def api(host):
    api = TestRailAPI(host, 'example@mail.com', 'password')
    yield api
