import json

import pytest
import responses


def add_suite(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({"id": 1, "name": data["name"], "description": data["description"]})


def get_suites(req):
    return (
        200,
        {},
        json.dumps(
            {
                "offset": int(req.params.get("offset", 0)),
                "limit": int(req.params.get("limit", 250)),
                "size": 2,
                "suites": [
                    {"id": 1, "description": "Suite1"},
                    {"id": 2, "description": "Suite2"},
                ],
            }
        ),
    )


def test_get_suite(api, mock, url):
    mock.add_callback(
        responses.GET, url("get_suite/4"), lambda _: (200, {}, json.dumps({"id": 4, "description": "My suite"}))
    )
    resp = api.suites.get_suite(4)
    assert resp["id"] == 4


@pytest.mark.parametrize(("offset", "limit"), ((None, None), (0, 250), (2, 14)))
def test_get_suites(api, mock, url, offset, limit):
    mock.add_callback(responses.GET, url("get_suites/5"), get_suites)
    resp = api.suites.get_suites(5, offset=offset, limit=limit)
    assert resp["offset"] == (offset if offset is not None else 0)
    assert resp["limit"] == (limit if limit is not None else 250)
    assert resp["suites"][0]["id"] == 1
    assert resp["suites"][1]["description"] == "Suite2"


def test_add_suite(api, mock, url):
    mock.add_callback(responses.POST, url("add_suite/7"), add_suite)
    resp = api.suites.add_suite(7, "New suite", description="My new suite")
    assert resp["name"] == "New suite"
    assert resp["description"] == "My new suite"


def test_update_suite(api, mock, url):
    mock.add_callback(responses.POST, url("update_suite/4"), add_suite)
    resp = api.suites.update_suite(4, name="new name", description="new description")
    assert resp["name"] == "new name"
    assert resp["description"] == "new description"


def test_delete_suite(api, mock, url):
    mock.add_callback(responses.POST, url("delete_suite/4"), lambda _: (200, {}, ""))
    resp = api.suites.delete_suite(4)
    assert resp is None
