import json

import responses


def add_section(r):
    data = json.loads(r.body)
    return 200, {}, json.dumps({'id': 2, 'name': data['name'], 'description': data['description']})


def test_get_section(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_section/3',
        lambda x: (200, {}, json.dumps({'depth': 1, 'description': 'My section'}))
    )
    resp = api.sections.get_section(3)
    assert resp['depth'] == 1


def test_get_sections(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_sections/5&suite_id=2',
        lambda x: (200, {}, json.dumps([{'depth': 1, 'description': 'My section'}]))
    )
    resp = api.sections.get_sections(5, suite_id=2)
    assert resp[0]['depth'] == 1


def test_add_section(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/add_section/4',
        add_section
    )
    resp = api.sections.add_section(4, 'new section', suite_id=2, description='Description')
    assert resp['name'] == 'new section'
    assert resp['description'] == 'Description'


def test_update_section(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/update_section/2',
        add_section
    )
    resp = api.sections.update_section(2, name='new_name', description='new_description')
    assert resp['name'] == 'new_name'
    assert resp['description'] == 'new_description'


def test_delete_section(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/delete_section/2',
        lambda x: (200, {}, '')
    )
    resp = api.sections.delete_section(2)
    assert resp is None
