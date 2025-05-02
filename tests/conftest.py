import os
from collections.abc import Iterator
from pathlib import Path
from typing import Callable

import pytest
import responses

try:
    from responses import FalseBool

    false_bool = FalseBool()
except ImportError:
    false_bool = False

from testrail_api import TestRailAPI

BASE_HOST = "https://example.testrail.com/index.php?/api/v2/"


class CallbackResponse(responses.CallbackResponse):
    def _url_matches(self, url: str, other: str, match_querystring=false_bool) -> bool:  # noqa: ARG002
        base_url = url.replace(BASE_HOST, "")
        other = other.replace(BASE_HOST, "")
        base_other = other.split("&", 1)[0]
        return base_url == base_other


class RequestsMock(responses.RequestsMock):
    def add_callback(
        self,
        method,
        url,
        callback,
        match_querystring=false_bool,
        content_type="text/plain",
        match=(),
    ) -> None:
        """Request callback method."""
        self._registry.add(
            CallbackResponse(
                url=url,
                method=method,
                callback=callback,
                content_type=content_type,
                match_querystring=match_querystring,
                match=match,
            )
        )


@pytest.fixture(scope="session")
def host() -> str:
    """Test host."""
    return "https://example.testrail.com/"


@pytest.fixture(scope="session")
def url(host: str) -> Callable[[str], str]:
    """Compiled url."""

    def _wrap(endpoint: str) -> str:
        return f"{host}index.php?/api/v2/{endpoint}"

    return _wrap


@pytest.fixture(scope="session")
def base_path() -> str:
    """Root path."""
    path = Path(__file__).absolute().parent
    return str(path)


@pytest.fixture(scope="session")
def auth_data(host: str) -> tuple[str, str, str]:
    """Test data for authorization."""
    return host, "example@mail.com", "password"


@pytest.fixture
def mock() -> Iterator[RequestsMock]:
    """Mock request."""
    with RequestsMock() as resp:
        yield resp


@pytest.fixture
def api(auth_data: tuple[str, str, str]) -> TestRailAPI:
    """TestRailAPI object."""
    return TestRailAPI(*auth_data)


@pytest.fixture
def environ(auth_data: tuple[str, str, str]) -> Iterator[None]:
    """Set envs."""
    os.environ["TESTRAIL_URL"] = auth_data[0]
    os.environ["TESTRAIL_EMAIL"] = auth_data[1]
    os.environ["TESTRAIL_PASSWORD"] = auth_data[2]
    yield
    del os.environ["TESTRAIL_URL"]
    del os.environ["TESTRAIL_EMAIL"]
    del os.environ["TESTRAIL_PASSWORD"]
