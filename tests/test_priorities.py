import json

import responses


def test_get_priorities(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_priorities"),
        lambda _: (200, {}, json.dumps([{"id": 1, "priority": 1}, {"id": 4, "priority": 4}])),
    )

    resp = api.priorities.get_priorities()
    assert resp[0]["id"] == 1
    assert resp[1]["priority"] == 4
