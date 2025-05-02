import json

import responses


def test_get_statuses(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_statuses"),
        lambda _: (200, {}, json.dumps([{"id": 1, "label": "Passed"}, {"id": 5, "label": "Failed"}])),
    )
    resp = api.statuses.get_statuses()
    assert resp[0]["id"] == 1
    assert resp[1]["label"] == "Failed"


def test_get_case_statuses(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_case_statuses"),
        lambda _: (
            200,
            {},
            json.dumps(
                [
                    {
                        "case_status_id": 1,
                        "name": "Approved",
                        "abbreviation": None,
                        "is_default": False,
                        "is_approved": True,
                    },
                    {
                        "case_status_id": 2,
                        "name": "Draft",
                        "abbreviation": None,
                        "is_default": True,
                        "is_approved": True,
                    },
                ]
            ),
        ),
    )
    resp = api.statuses.get_case_statuses()
    assert resp[0]["case_status_id"] == 1
    assert resp[1]["name"] == "Draft"
