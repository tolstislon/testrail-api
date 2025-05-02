import json

import responses


def add_case_field(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({"id": 33, "type_id": 12, "label": data["label"], "description": data["description"]})


def test_get_case_fields(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_case_fields"),
        lambda _: (200, {}, json.dumps([{"id": 1, "description": "The preconditions of this test case"}])),
    )
    resp = api.case_fields.get_case_fields()
    assert resp[0]["id"] == 1


def test_add_case_field(api, mock, url):
    mock.add_callback(responses.POST, url("add_case_field"), add_case_field)
    resp = api.case_fields.add_case_field(
        "Integer",
        "My field",
        "label",
        description="New field",
        configs=[
            {
                "context": {"is_global": True, "project_ids": []},
                "options": {"is_required": True, "default_value": "1", "items": "1, First\n2, Second"},
            }
        ],
    )
    assert resp["label"] == "label"
    assert resp["description"] == "New field"
