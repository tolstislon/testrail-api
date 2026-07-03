import json
import random

import responses
from requests import PreparedRequest


def _get_dynamic_filter_fields(_: PreparedRequest) -> tuple[int, dict, str]:
    return (
        200,
        {},
        json.dumps(
            [
                {
                    "type_id": 6,
                    "system_name": "priority_id",
                    "label": "Priority",
                    "options": {},
                    "sub_filters": [],
                }
            ]
        ),
    )


def test_get_dynamic_filter_fields(api, mock):
    project_id = random.randint(1, 1000)
    mock.add_callback(responses.GET, f"get_dynamic_filter_fields/{project_id}", _get_dynamic_filter_fields)
    resp = api.dynamic_filter_fields.get_dynamic_filter_fields(project_id)
    assert resp[0]["system_name"] == "priority_id"
    assert resp[0]["type_id"] == 6
