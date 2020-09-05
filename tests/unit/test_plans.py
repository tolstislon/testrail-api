import json
import re
from datetime import datetime

import pytest
import responses


def get_plans(r):
    assert r.params['is_completed'] == '1'
    for key in 'created_after', 'created_before':
        assert re.match(r'^\d+$', r.params[key])
    return 200, {}, json.dumps([{'id': 5, 'name': 'System test'}])


def add_plan(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps(
        {'id': 96, 'name': data['name'], 'milestone_id': data['milestone_id']}
    )


def add_run_to_plan_entry(r):
    data = json.loads(r.body.decode())
    assert data['config_ids'] == [1, 2]
    return 200, {}, ''


def update_run_in_plan_entry(r):
    data = json.loads(r.body.decode())
    assert data['description'] == 'Test'
    return 200, {}, ''


def add_plan_entry(r):
    data = json.loads(r.body.decode())
    assert data['include_all'] is True
    assert data['config_ids'] == [1, 2, 3]
    return 200, {}, json.dumps({'id': 5, 'name': 'System test'})


def update_plan_entry(r):
    data = json.loads(r.body.decode())
    assert data['case_ids'] == [2, 3]
    return 200, {}, json.dumps({'id': 7, 'name': data['name']})


def test_get_plan(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_plan/5'.format(host),
        lambda x: (200, {}, json.dumps({'id': 5, 'name': 'System test'}))
    )
    resp = api.plans.get_plan(5)
    assert resp['id'] == 5


@pytest.mark.parametrize('is_completed', (1, True))
def test_get_plans(api, mock, host, is_completed):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_plans/7'.format(host),
        get_plans
    )
    resp = api.plans.get_plans(
        7, is_completed=is_completed, created_after=datetime.now(), created_before=datetime.now()
    )
    assert resp[0]['id'] == 5


def test_add_plan(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_plan/5'.format(host),
        add_plan
    )
    resp = api.plans.add_plan(5, name='new plan', milestone_id=4)
    assert resp['name'] == 'new plan'
    assert resp['milestone_id'] == 4


def test_add_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_plan_entry/7'.format(host),
        add_plan_entry
    )
    resp = api.plans.add_plan_entry(7, 3, include_all=True, config_ids=[1, 2, 3])
    assert resp['id'] == 5


def test_update_plan(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/update_plan/12'.format(host),
        add_plan
    )
    resp = api.plans.update_plan(12, name='update', milestone_id=1)
    assert resp['name'] == 'update'
    assert resp['milestone_id'] == 1


def test_update_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/update_plan_entry/7/1'.format(host),
        update_plan_entry
    )
    resp = api.plans.update_plan_entry(7, 1, name='Update name', case_ids=[2, 3])
    assert resp['name'] == 'Update name'


def test_close_plan(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/close_plan/7'.format(host),
        lambda x: (200, {}, json.dumps({'id': 7, 'name': 'System test'}))
    )
    resp = api.plans.close_plan(7)
    assert resp['id'] == 7


def test_delete_plan(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_plan/11'.format(host),
        lambda x: (200, {}, '')
    )
    resp = api.plans.delete_plan(11)
    assert resp is None


def test_delete_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_plan_entry/12/2'.format(host),
        lambda x: (200, {}, '')
    )
    resp = api.plans.delete_plan_entry(12, 2)
    assert resp is None


def test_add_run_to_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_run_to_plan_entry/12/2'.format(host),
        add_run_to_plan_entry
    )
    api.plans.add_run_to_plan_entry(12, 2, [1, 2])


def test_update_run_in_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/update_run_in_plan_entry/12/2'.format(host),
        update_run_in_plan_entry
    )
    api.plans.update_run_in_plan_entry(12, 2, description='Test')


def test_delete_run_from_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_run_from_plan_entry/2'.format(host),
        lambda x: (200, {}, '')
    )
    api.plans.delete_run_from_plan_entry(2)
