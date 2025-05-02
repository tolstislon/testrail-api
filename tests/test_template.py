import json

import responses


def test_get_templates(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_templates/1"),
        lambda _: (
            200,
            {},
            json.dumps([{"id": 1, "name": "Test Case (Text)"}, {"id": 2, "name": "Test Case (Steps)"}]),
        ),
    )
    resp = api.templates.get_templates(1)
    assert resp[0]["id"] == 1
    assert resp[1]["name"] == "Test Case (Steps)"
