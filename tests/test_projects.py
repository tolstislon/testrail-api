import json

import pytest
import responses


def get_projects(r):
    assert r.params["is_completed"] == "0"
    return 200, {}, json.dumps([{"id": 1, "name": "Datahub"}])


def add_project(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({"id": 1, "name": data["name"]})


def update_project(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({"id": 1, "name": "Datahub", "is_completed": data["is_completed"]})


def test_get_project(api, mock, url):
    mock.add_callback(
        responses.GET, url("get_project/1"), lambda _: (200, {}, json.dumps({"id": 1, "name": "Datahub"}))
    )
    resp = api.projects.get_project(1)
    assert resp["name"] == "Datahub"


@pytest.mark.parametrize("is_completed", (0, False))
def test_get_projects(api, mock, url, is_completed):
    mock.add_callback(
        responses.GET,
        url("get_projects"),
        get_projects,
    )
    resp = api.projects.get_projects(is_completed=is_completed)
    assert resp[0]["name"] == "Datahub"


def test_add_project(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("add_project"),
        add_project,
    )
    resp = api.projects.add_project("My project", announcement="description", show_announcement=True, suite_mode=1)
    assert resp["name"] == "My project"


@pytest.mark.parametrize("is_completed", (True, False))
def test_update_project(api, mock, url, is_completed):
    mock.add_callback(
        responses.POST,
        url("update_project/1"),
        update_project,
    )
    resp = api.projects.update_project(1, is_completed=is_completed)
    assert resp["is_completed"] is is_completed


def test_delete_project(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("delete_project/1"),
        lambda _: (200, {}, ""),
    )
    resp = api.projects.delete_project(1)
    assert resp is None
