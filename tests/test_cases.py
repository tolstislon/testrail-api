import json
import re
from datetime import datetime
from functools import partial

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
    return 200, {}, json.dumps(
        {'id': 1, 'title': data['title'], 'priority_id': data['priority_id']})


def update_case(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({'id': 1, 'title': data['title']})


def update_cases_suite(r, suite_id=None):
    if suite_id:
        assert int(r.params['suite_id']) == suite_id
    return 200, {}, r.body.decode()


def delete_cases(r, project_id=None, case_ids=None, suite_id=None, soft=0):
    assert int(r.params['soft']) == soft
    assert int(r.params['project_id']) == project_id
    if suite_id:
        assert 'delete_cases/{}&'.format(suite_id) in r.url
    else:
        assert 'delete_cases&' in r.url
    assert json.loads(r.body.decode()) == {'case_ids': case_ids}
    return 200, {}, ''


def test_get_case(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_case/1'),
        lambda x: (200, {}, json.dumps({'id': 1, 'type_id': 1, 'title': 'My case'})),
    )
    resp = api.cases.get_case(1)
    assert resp['id'] == 1


def test_get_cases(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_cases/1'),
        get_cases,
    )
    now = datetime.now()

    resp = api.cases.get_cases(
        1, suite_id=2, section_id=3, limit=5, offset=10,
        created_after=now, created_before=round(now.timestamp()),
        updated_after=now, updated_before=now
    )
    assert resp[0]['id'] == 1


def test_add_case(api, mock, url):
    mock.add_callback(
        responses.POST,
        url('add_case/2'),
        add_case,
    )
    resp = api.cases.add_case(2, 'New case', priority_id=1)
    assert resp['title'] == 'New case'
    assert resp['priority_id'] == 1


def test_update_case(api, mock, url):
    mock.add_callback(
        responses.POST,
        url('update_case/1'),
        update_case,
    )
    resp = api.cases.update_case(1, title='New case title')
    assert resp['title'] == 'New case title'


def test_delete_case(api, mock, url):
    mock.add_callback(
        responses.POST,
        url('delete_case/5'),
        lambda x: (200, {}, ''),
    )
    resp = api.cases.delete_case(5)
    assert resp is None


def test_get_history_for_case(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_history_for_case/7'),
        lambda x: (200, {}, ''),
    )
    api.cases.get_history_for_case(7)


def test_update_cases_no_suite(api, mock, url):
    mock.add_callback(
        responses.POST,
        url('update_case/1'),
        update_cases_suite,
    )
    body = {'priority_id': 1, 'estimate': '5m'}
    resp = api.cases.update_cases(1, **body)
    assert resp == body


def test_update_cases_suite(api, mock, url):
    mock.add_callback(
        responses.POST,
        url('update_case/1'),
        partial(update_cases_suite, suite_id=2),
    )
    body = {'priority_id': 1, 'estimate': '5m'}
    resp = api.cases.update_cases(1, 2, **body)
    assert resp == body


def test_delete_cases_no_suite_id(api, mock, url):
    mock.add_callback(
        responses.POST,
        url('delete_cases'),
        partial(delete_cases, project_id=1, case_ids=[5, 6]),
    )
    api.cases.delete_cases(1, [5, 6])


def test_delete_cases_suite_id(api, mock, url):
    mock.add_callback(
        responses.POST,
        url('delete_cases/1'),
        partial(delete_cases, project_id=1, suite_id=1, case_ids=[5, 6]),
    )
    api.cases.delete_cases(1, [5, 6], 1)


def test_delete_cases_suite_id_soft(api, mock, url):
    mock.add_callback(
        responses.POST,
        url('delete_cases/1'),
        partial(delete_cases, project_id=1, suite_id=1, soft=1, case_ids=[5, 6]),
    )
    api.cases.delete_cases(1, [5, 6], 1, 1)
