import json

import responses


def test_get_result_fields(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_result_fields'.format(host),
        lambda x: (200, {}, json.dumps([{'id': 1, 'configs': []}]))
    )
    resp = api.result_fields.get_result_fields()
    assert resp[0]['id'] == 1
