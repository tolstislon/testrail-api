import json

import responses


def test_get_templates(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_templates/1'.format(host),
        lambda x: (200, {}, json.dumps([{'id': 1, 'name': 'Test Case (Text)'}, {'id': 2, 'name': 'Test Case (Steps)'}]))
    )
    resp = api.templates.get_templates(1)
    assert resp[0]['id'] == 1
    assert resp[1]['name'] == 'Test Case (Steps)'
