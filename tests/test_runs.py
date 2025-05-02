import json
import re
from datetime import datetime

import pytest
import responses


def get_runs(r):
    assert r.params["is_completed"] == "1"
    for key in "created_after", "created_before":
        assert re.match(r"^\d+$", r.params[key])
    return (
        200,
        {},
        json.dumps(
            {
                "offset": 0,
                "limit": 250,
                "size": 1,
                "runs": [{"id": 1, "name": "My run", "is_completed": r.params["is_completed"]}],
            }
        ),
    )


def add_run(r):
    data = json.loads(r.body.decode())
    return (
        200,
        {},
        json.dumps(
            {"id": 25, "suite_id": data["suite_id"], "name": data["name"], "milestone_id": data["milestone_id"]}
        ),
    )


def test_get_run(api, mock, url):
    mock.add_callback(responses.GET, url("get_run/1"), lambda _: (200, {}, json.dumps({"id": 1, "name": "My run"})))
    resp = api.runs.get_run(1)
    assert resp["id"] == 1


@pytest.mark.parametrize("is_completed", (1, True))
def test_get_runs(api, mock, url, is_completed):
    mock.add_callback(responses.GET, url("get_runs/12"), get_runs)
    resp = api.runs.get_runs(
        12, is_completed=is_completed, created_after=datetime.now(), created_before=datetime.now()
    ).get("runs")
    assert resp[0]["is_completed"] == "1"


def test_add_run(api, mock, url):
    mock.add_callback(responses.POST, url("add_run/12"), add_run)
    resp = api.runs.add_run(12, suite_id=1, name="New Run", milestone_id=1)
    assert resp["suite_id"] == 1
    assert resp["name"] == "New Run"
    assert resp["milestone_id"] == 1


def test_update_run(api, mock, url):
    mock.add_callback(responses.POST, url("update_run/15"), add_run)
    resp = api.runs.update_run(15, suite_id=1, name="New Run", milestone_id=1)
    assert resp["suite_id"] == 1
    assert resp["name"] == "New Run"
    assert resp["milestone_id"] == 1


def test_close_run(api, mock, url):
    mock.add_callback(
        responses.POST, url("close_run/3"), lambda _: (200, {}, json.dumps({"id": 3, "is_completed": True}))
    )
    resp = api.runs.close_run(3)
    assert resp["is_completed"] is True


def test_delete_run(api, mock, url):
    mock.add_callback(responses.POST, url("delete_run/2"), lambda _: (200, {}, ""))
    resp = api.runs.delete_run(2)
    assert resp is None


@pytest.mark.parametrize("is_completed", (1, True))
def test_get_runs_bulk(api, mock, url, is_completed):
    mock.add_callback(responses.GET, url("get_runs/12"), get_runs)
    resp = api.runs.get_runs_bulk(
        12, is_completed=is_completed, created_after=datetime.now(), created_before=datetime.now()
    )
    assert resp[0]["is_completed"] == "1"
