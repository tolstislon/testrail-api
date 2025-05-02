import json
from datetime import datetime

import pytest
import responses


def add_milestone(r):
    req = json.loads(r.body.decode())
    req["id"] = 1
    assert isinstance(req["start_on"], int)
    assert isinstance(req["due_on"], int)
    return 200, {}, json.dumps(req)


def get_milestones(r):
    req = r.params
    assert req["is_started"] == "1"
    return (
        200,
        {},
        json.dumps(
            {
                "offset": 250,
                "limit": 250,
                "size": 1,
                "milestones": [{"id": 1, "name": "Milestone 1", "description": "My new milestone"}],
            }
        ),
    )


def update_milestone(r):
    req = json.loads(r.body.decode())
    req["id"] = 1
    assert isinstance(req["start_on"], int)
    return 200, {}, json.dumps(req)


def test_get_milestone(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_milestone/1"),
        lambda _: (200, {}, json.dumps({"id": 1, "name": "Milestone 1", "description": "My new milestone"})),
        content_type="application/json",
    )
    response = api.milestones.get_milestone(1)
    assert response["name"] == "Milestone 1"
    assert response["description"] == "My new milestone"


@pytest.mark.parametrize("is_started", (1, True))
def test_get_milestones(api, mock, url, is_started):
    mock.add_callback(responses.GET, url("get_milestones/1"), get_milestones, content_type="application/json")
    response = api.milestones.get_milestones(project_id=1, is_started=is_started).get("milestones")
    assert response[0]["name"] == "Milestone 1"
    assert response[0]["description"] == "My new milestone"


def test_add_milestone(api, mock, url):
    mock.add_callback(responses.POST, url("add_milestone/1"), add_milestone, content_type="application/json")
    response = api.milestones.add_milestone(
        project_id=1,
        name="New milestone",
        start_on=datetime.now(),
        due_on=int(datetime.now().timestamp()),
        description="My new milestone",
    )
    assert response["name"] == "New milestone"
    assert response["description"] == "My new milestone"


def test_update_milestone(api, mock, url):
    mock.add_callback(responses.POST, url("update_milestone/1"), update_milestone, content_type="application/json")
    response = api.milestones.update_milestone(1, is_completed=True, parent_id=23, start_on=datetime.now())
    assert response["is_completed"] is True
    assert response["parent_id"] == 23


def test_delete_milestone(api, mock, url):
    mock.add_callback(
        responses.POST, url("delete_milestone/1"), lambda _: (200, {}, ""), content_type="application/json"
    )
    response = api.milestones.delete_milestone(1)
    assert response is None


def test_get_milestones_bulk(api, mock, url):
    mock.add_callback(responses.GET, url("get_milestones/1"), get_milestones, content_type="application/json")
    response = api.milestones.get_milestones_bulk(1, is_started=1)
    assert response[0]["name"] == "Milestone 1"
    assert response[0]["description"] == "My new milestone"
