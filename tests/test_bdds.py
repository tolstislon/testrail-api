import json
from functools import partial
from pathlib import Path

import pytest
import responses

from testrail_api import StatusCodeError


def add_bdd(r):
    assert "multipart/form-data" in r.headers["Content-Type"]
    assert r.headers["User-Agent"].startswith("Python TestRail API v:")
    assert r.body
    return 200, {}, json.dumps({"id": 1, "title": "BDD case"})


def get_bdd(_, path):
    file = Path(path, "attach.jpg")
    with file.open("rb") as f:
        return 200, {}, f


def test_add_bdd(api, mock, url, base_path):
    mock.add_callback(responses.POST, url("add_bdd/188"), add_bdd)
    file = Path(base_path, "attach.jpg")
    resp = api.bdds.add_bdd(188, file)
    assert resp["id"] == 1


def test_add_bdd_str(api, mock, url, base_path):
    mock.add_callback(responses.POST, url("add_bdd/188"), add_bdd)
    file = Path(base_path, "attach.jpg")
    resp = api.bdds.add_bdd(188, str(file))
    assert resp["id"] == 1


def test_get_bdd(api, mock, url, base_path):
    mock.add_callback(responses.GET, url("get_bdd/2133"), partial(get_bdd, path=base_path))
    file = Path(base_path, "new_bdd.feature")
    new_file = api.bdds.get_bdd(2133, file)
    assert new_file.exists()
    new_file.unlink()


def test_get_bdd_str(api, mock, url, base_path):
    mock.add_callback(responses.GET, url("get_bdd/2133"), partial(get_bdd, path=base_path))
    file = Path(base_path, "new_bdd_str.feature")
    new_file = api.bdds.get_bdd(2133, str(file))
    assert new_file.exists()
    new_file.unlink()


def test_get_bdd_error(api, mock, url, base_path):
    mock.add_callback(responses.GET, url("get_bdd/2133"), lambda _: (400, {}, ""))
    file = Path(base_path, "new_bdd.feature")
    with pytest.raises(StatusCodeError):
        new_file = api.bdds.get_bdd(2133, str(file))
        assert new_file is None
