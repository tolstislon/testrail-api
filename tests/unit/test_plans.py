import json

import responses


def get_plans(r):
    assert r.params['is_completed'] == '1'
    return 200, {}, json.dumps([{'id': 5, 'name': 'System test'}])


def add_plan(r):
    data = json.loads(r.body)
    return 200, {}, json.dumps({'id': 96, 'name': data['name'], 'milestone_id': data['milestone_id']})


def add_plan_entry(r):
    data = json.loads(r.body)
    assert data['include_all'] is True
    assert data['config_ids'] == [1, 2, 3]
    return 200, {}, json.dumps({'id': 5, 'name': 'System test'})


def update_plan_entry(r):
    data = json.loads(r.body)
    assert data['case_ids'] == [2, 3]
    return 200, {}, json.dumps({'id': 7, 'name': data['name']})


def test_get_plan(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_plan/5',
        lambda x: (200, {}, json.dumps({'id': 5, 'name': 'System test'}))
    )
    resp = api.plans.get_plan(5)
    assert resp['id'] == 5


def test_get_plans(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_plans/7',
        get_plans
    )
    resp = api.plans.get_plans(7, is_completed=1)
    assert resp[0]['id'] == 5


def test_add_plan(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/add_plan/5',
        add_plan
    )
    resp = api.plans.add_plan(5, name='new plan', milestone_id=4)
    assert resp['name'] == 'new plan'
    assert resp['milestone_id'] == 4


def test_add_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/add_plan_entry/7',
        add_plan_entry
    )
    resp = api.plans.add_plan_entry(7, 3, include_all=True, config_ids=[1, 2, 3])
    assert resp['id'] == 5


def test_update_plan(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/update_plan/12',
        add_plan
    )
    resp = api.plans.update_plan(12, name='update', milestone_id=1)
    assert resp['name'] == 'update'
    assert resp['milestone_id'] == 1


def test_update_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/update_plan_entry/7/1',
        update_plan_entry
    )
    resp = api.plans.update_plan_entry(7, 1, name='Update name', case_ids=[2, 3])
    assert resp['name'] == 'Update name'


def test_close_plan(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/close_plan/7',
        lambda x: (200, {}, json.dumps({'id': 7, 'name': 'System test'}))
    )
    resp = api.plans.close_plan(7)
    assert resp['id'] == 7


def test_delete_plan(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/delete_plan/11',
        lambda x: (200, {}, '')
    )
    resp = api.plans.delete_plan(11)
    assert resp is None


def test_delete_plan_entry(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/delete_plan_entry/12/2',
        lambda x: (200, {}, '')
    )
    resp = api.plans.delete_plan_entry(12, 2)
    assert resp is None
