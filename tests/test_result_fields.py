import json

import responses


def test_get_result_fields(api, mock, url):
    mock.add_callback(
        responses.GET, url("get_result_fields"), lambda _: (200, {}, json.dumps([{"id": 1, "configs": []}]))
    )
    resp = api.result_fields.get_result_fields()
    assert resp[0]["id"] == 1
