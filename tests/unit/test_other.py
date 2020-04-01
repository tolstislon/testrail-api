import json
from functools import partial
from pathlib import Path
import pytest
import responses
import time
from testrail_api import StatusCodeError, TestRailAPI


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


def test_rate_limit(api, mock, host):
    limit = RateLimit()
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_cases/1',
        limit.rate,
    )
    resp = api.cases.get_case(1)
    assert resp['count'] == 2


def test_raise_rate_limit(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_cases/1',
        lambda x: (429, {}, ''),
    )
    with pytest.raises(StatusCodeError):
        api.cases.get_case(1)


def test_ex_raise_rate_limit(auth_data, mock, host):
    api = TestRailAPI(*auth_data, exc=True)
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_cases/1',
        lambda x: (429, {}, ''),
    )
    resp = api.cases.get_case(1)
    assert resp is None
