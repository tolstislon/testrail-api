import json

import responses


def test_get_case_types(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_case_types"),
        lambda _: (200, {}, json.dumps([{"id": 1, "name": "Automated"}, {"id": 6, "name": "Other"}])),
    )
    resp = api.case_types.get_case_types()
    assert resp[0]["id"] == 1
    assert resp[1]["name"] == "Other"
