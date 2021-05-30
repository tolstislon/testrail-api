import json

import responses


def test_get_statuses(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_statuses'.format(host),
        lambda x: (200, {}, json.dumps([{'id': 1, 'label': 'Passed'}, {'id': 5, 'label': 'Failed'}]))
    )
    resp = api.statuses.get_statuses()
    assert resp[0]['id'] == 1
    assert resp[1]['label'] == 'Failed'
