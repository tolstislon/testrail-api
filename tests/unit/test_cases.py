import json
import re
from datetime import datetime

import responses


def get_cases(r):
    assert r.params['suite_id']
    assert r.params['section_id']
    assert r.params['limit']
    assert r.params['offset']
    for key in 'created_after', 'created_before', 'updated_after', 'updated_before':
        assert re.match(r'^\d+$', r.params[key])
    return 200, {}, json.dumps([{'id': 1, 'type_id': 1, 'title': 'My case'}])


def add_case(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({'id': 1, 'title': data['title'], 'priority_id': data['priority_id']})


def update_case(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({'id': 1, 'title': data['title']})


def test_get_case(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case/1'.format(host),
        lambda x: (200, {}, json.dumps({'id': 1, 'type_id': 1, 'title': 'My case'})),
    )
    resp = api.cases.get_case(1)
    assert resp['id'] == 1


def test_get_cases(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_cases/1'.format(host),
        get_cases,
    )
    now = datetime.now()

    resp = api.cases.get_cases(
        1, suite_id=2, section_id=3, limit=5, offset=10,
        created_after=now, created_before=round(now.timestamp()), updated_after=now, updated_before=now
    )
    assert resp[0]['id'] == 1


def test_add_case(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_case/2'.format(host),
        add_case,
    )
    resp = api.cases.add_case(2, 'New case', priority_id=1)
    assert resp['title'] == 'New case'
    assert resp['priority_id'] == 1


def test_update_case(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/update_case/1'.format(host),
        update_case,
    )
    resp = api.cases.update_case(1, title='New case title')
    assert resp['title'] == 'New case title'


def test_delete_case(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_case/5'.format(host),
        lambda x: (200, {}, ''),
    )
    resp = api.cases.delete_case(5)
    assert resp is None
