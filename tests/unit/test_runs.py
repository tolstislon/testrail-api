import json

import pytest
import responses


def get_runs(r):
    assert r.params['is_completed'] == '1'
    return 200, {}, json.dumps([{'id': 1, 'name': 'My run', 'is_completed': r.params['is_completed']}])


def add_run(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps(
        {'id': 25, 'suite_id': data['suite_id'], 'name': data['name'], 'milestone_id': data['milestone_id']}
    )


def test_get_run(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_run/1'.format(host),
        lambda x: (200, {}, json.dumps({'id': 1, 'name': 'My run'}))
    )
    resp = api.runs.get_run(1)
    assert resp['id'] == 1


@pytest.mark.parametrize('is_completed', (1, True))
def test_get_runs(api, mock, host, is_completed):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_runs/12'.format(host),
        get_runs
    )
    resp = api.runs.get_runs(12, is_completed=is_completed)
    assert resp[0]['is_completed'] == '1'


def test_add_run(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_run/12'.format(host),
        add_run
    )
    resp = api.runs.add_run(12, suite_id=1, name='New Run', milestone_id=1)
    assert resp['suite_id'] == 1
    assert resp['name'] == 'New Run'
    assert resp['milestone_id'] == 1


def test_update_run(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/update_run/15'.format(host),
        add_run
    )
    resp = api.runs.update_run(15, suite_id=1, name='New Run', milestone_id=1)
    assert resp['suite_id'] == 1
    assert resp['name'] == 'New Run'
    assert resp['milestone_id'] == 1


def test_close_run(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/close_run/3'.format(host),
        lambda x: (200, {}, json.dumps({'id': 3, 'is_completed': True}))
    )
    resp = api.runs.close_run(3)
    assert resp['is_completed'] is True


def test_delete_run(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_run/2'.format(host),
        lambda x: (200, {}, '')
    )
    resp = api.runs.delete_run(2)
    assert resp is None
