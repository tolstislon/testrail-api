import json
import random
from datetime import datetime

import pytest
import responses


def get_labels(req):
    return (
        200,
        {},
        json.dumps(
            {
                "offset": int(req.params.get("offset", 0)),
                "limit": int(req.params.get("limit", 250)),
                "size": 2,
                "labels": [
                    {"id": 3, "title": "Tester", "created_by": "2", "created_on": datetime.timestamp(datetime.now())},
                    {"id": 1, "title": "Lead", "created_by": "2", "created_on": datetime.timestamp(datetime.now())},
                ],
            }
        ),
    )


def update_label(req):
    body = json.loads(req.body)
    return (
        200,
        {},
        json.dumps(
            {
                "id": random.randint(1, 100),
                "title": body["title"],
            }
        ),
    )


def test_get_label(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_label/1"),
        lambda _: (200, {}, json.dumps({"id": 1, "name": "Label 1", "created_by": "2"})),
        content_type="application/json",
    )
    response = api.labels.get_label("1")
    assert response["name"] == "Label 1"
    assert response["created_by"] == "2"


@pytest.mark.parametrize(("offset", "limit"), ((None, None), (0, 250), (2, 14)))
def test_get_labels(api, mock, url, offset, limit):
    mock.add_callback(responses.GET, url("get_labels/1"), get_labels, content_type="application/json")
    response = api.labels.get_labels(project_id=1, offset=offset, limit=limit)
    assert response["offset"] == (offset if offset is not None else 0)
    assert response["limit"] == (limit if limit is not None else 250)
    assert len(response["labels"]) == 2


def test_update_label(api, mock, url):
    mock.add_callback(responses.POST, url("update_label/1"), update_label, content_type="application/json")
    project_id = random.randint(1, 100)
    title = f"Test {random.randint(1, 100)}"
    response = api.labels.update_label(1, project_id=project_id, title=title)
    assert response["title"] == title
    assert isinstance(response["id"], int)
