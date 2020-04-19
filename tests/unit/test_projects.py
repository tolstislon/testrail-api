import json

import responses


def get_projects(r):
    assert r.params['is_completed'] == '0'
    return 200, {}, json.dumps([{'id': 1, 'name': 'Datahub'}])


def add_project(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({'id': 1, 'name': data['name']})


def update_project(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({'id': 1, 'name': 'Datahub', 'is_completed': data['is_completed']})


def test_get_project(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_project/1'.format(host),
        lambda x: (200, {}, json.dumps({'id': 1, 'name': 'Datahub'}))
    )
    resp = api.projects.get_project(1)
    assert resp['name'] == 'Datahub'


def test_get_projects(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_projects'.format(host),
        get_projects,
    )
    resp = api.projects.get_projects(is_completed=0)
    assert resp[0]['name'] == 'Datahub'


def test_add_project(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_project'.format(host),
        add_project,
    )
    resp = api.projects.add_project('My project', announcement='description', show_announcement=True, suite_mode=1)
    assert resp['name'] == 'My project'


def test_update_project(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/update_project/1'.format(host),
        update_project,
    )
    resp = api.projects.update_project(1, is_completed=True)
    assert resp['is_completed'] is True


def test_delete_project(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_project/1'.format(host),
        lambda x: (200, {}, ''),
    )
    resp = api.projects.delete_project(1)
    assert resp is None
