import json

import pytest
import responses


def get_tests(r):
    resp = [{'id': c, 'status_id': int(i)} for c, i in enumerate(r.params['status_id'].split(','), 1)]
    return 200, {}, json.dumps(resp)


def test_get_test(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_test/2'.format(host),
        lambda x: (200, {}, json.dumps({'case_id': 1, 'id': 2, 'run_id': 2}))
    )
    resp = api.tests.get_test(2)
    assert resp['case_id'] == 1


@pytest.mark.parametrize('status_id', ('1,5', [1, 5]))
def test_get_tests(api, mock, host, status_id):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_tests/2'.format(host),
        get_tests
    )
    resp = api.tests.get_tests(2, status_id=status_id)
    assert resp[0]['status_id'] == 1
    assert resp[1]['status_id'] == 5
