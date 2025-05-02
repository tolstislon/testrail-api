import json

import pytest
import responses


def get_group(_):
    return 200, {}, json.dumps({"id": 1, "name": "New group", "user_ids": [1, 2, 3, 4, 5]})


def get_groups(_):
    return (
        200,
        {},
        json.dumps(
            {
                "offset": 0,
                "limit": 250,
                "size": 0,
                "_links": {
                    "next": None,
                    "prev": None,
                },
                "groups": [{"id": 1, "name": "New group", "user_ids": [1, 2, 3, 4, 5]}],
            }
        ),
    )


def add_group(r):
    req = json.loads(r.body)
    req["id"] = 1
    return 200, {}, json.dumps(req)


def test_get_group(api, mock, url):
    mock.add_callback(responses.GET, url("get_group/1"), get_group, content_type="application/json")
    resp = api.groups.get_group(1)
    assert resp["id"] == 1


def test_get_groups(api, mock, url):
    mock.add_callback(responses.GET, url("get_groups"), get_groups, content_type="application/json")
    resp = api.groups.get_groups()
    assert resp["groups"][0]["id"] == 1


def test_add_group(api, mock, url):
    mock.add_callback(responses.POST, url("add_group"), add_group, content_type="application/json")
    resp = api.groups.add_group("New group", [1, 2, 3, 4])
    assert resp["id"] == 1


@pytest.mark.parametrize("data", ({"name": "qwe"}, {"user_ids": [1, 2]}, {"name": "q", "user_ids": [1, 3]}))
def test_update_group(api, mock, url, data):
    mock.add_callback(responses.POST, url("update_group/1"), add_group, content_type="application/json")
    resp = api.groups.update_group(1, **data)
    for key in data:
        assert resp[key] == data[key]


def test_delete_group(api, mock, url):
    mock.add_callback(responses.POST, url("delete_group/1"), lambda _: (200, {}, ""), content_type="application/json")
    response = api.groups.delete_group(1)
    assert response is None
