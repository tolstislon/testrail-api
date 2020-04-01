import json

import responses


def add_suite(r):
    data = json.loads(r.body)
    return 200, {}, json.dumps({'id': 1, 'name': data['name'], 'description': data['description']})


def test_get_suite(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_suite/4',
        lambda x: (200, {}, json.dumps({'id': 4, 'description': 'My suite'}))
    )
    resp = api.suites.get_suite(4)
    assert resp['id'] == 4


def test_get_suites(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_suites/5',
        lambda x: (200, {}, json.dumps([{'id': 1, 'description': 'Suite1'}, {'id': 2, 'description': 'Suite2'}]))
    )
    resp = api.suites.get_suites(5)
    assert resp[0]['id'] == 1
    assert resp[1]['description'] == 'Suite2'


def test_add_suite(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/add_suite/7',
        add_suite
    )
    resp = api.suites.add_suite(5, 'New suite', description='My new suite')
    assert resp['name'] == 'New suite'
    assert resp['description'] == 'My new suite'


def test_update_suite(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/update_suite/4',
        add_suite
    )
    resp = api.suites.update_suite(4, name='new name', description='new description')
    assert resp['name'] == 'new name'
    assert resp['description'] == 'new description'


def test_delete_suite(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/delete_suite/4',
        lambda x: (200, {}, '')
    )
    resp = api.suites.delete_suite(4)
    assert resp is None
