import json

import responses


def add_shared_step(r):
    req = json.loads(r.body.decode())
    req["id"] = 1
    return 200, {}, json.dumps(req)


def test_get_shared_step(api, mock, url):
    mock.add_callback(
        responses.GET, url("get_shared_step/3"), lambda _: (200, {}, json.dumps({"id": 1, "title": "My step"}))
    )
    resp = api.shared_steps.get_shared_step(3)
    assert resp["id"] == 1
    assert resp["title"] == "My step"


def test_get_shared_steps(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_shared_steps/1"),
        lambda _: (
            200,
            {},
            json.dumps(
                {
                    "offset": 0,
                    "limit": 250,
                    "size": 1,
                    "shared_steps": [{"id": 1, "title": "My step"}],
                }
            ),
        ),
    )
    resp = api.shared_steps.get_shared_steps(project_id=1).get("shared_steps")
    assert resp[0]["id"] == 1
    assert resp[0]["title"] == "My step"


def test_add_shared_step(api, mock, url):
    mock.add_callback(responses.POST, url("add_shared_step/1"), add_shared_step)
    resp = api.shared_steps.add_shared_step(project_id=1, title="My step", custom_steps_separated=[{"a": 1}, {"b": 2}])
    assert resp["id"] == 1
    assert resp["title"] == "My step"


def test_update_shared_step(api, mock, url):
    mock.add_callback(responses.POST, url("update_shared_step/34"), add_shared_step)
    resp = api.shared_steps.update_shared_step(shared_update_id=34, title="New shared step")
    assert resp["title"] == "New shared step"


def test_delete_shared_step(api, mock, url):
    mock.add_callback(responses.POST, url("delete_shared_step/34"), lambda _: (200, {}, ""))
    api.shared_steps.delete_shared_step(shared_update_id=34)


def test_get_shared_steps_bulk(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_shared_steps/1"),
        lambda _: (
            200,
            {},
            json.dumps(
                {
                    "offset": 0,
                    "limit": 250,
                    "size": 1,
                    "shared_steps": [{"id": 1, "title": "My step"}],
                }
            ),
        ),
    )
    resp = api.shared_steps.get_shared_steps_bulk(project_id=1)
    assert resp[0]["id"] == 1
    assert resp[0]["title"] == "My step"
