import json

import responses


def add_case_field(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps(
        {'id': 33, 'type_id': 12, 'label': data['label'], 'description': data['description']}
    )


def test_get_case_fields(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_case_fields'.format(host),
        lambda x: (200, {}, json.dumps([{'id': 1, 'description': 'The preconditions of this test case'}]))
    )
    resp = api.case_fields.get_case_fields()
    assert resp[0]['id'] == 1


def test_add_case_field(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_case_field'.format(host),
        add_case_field
    )
    resp = api.case_fields.add_case_field('Integer', 'My field', 'label', description='New field')
    assert resp['label'] == 'label'
    assert resp['description'] == 'New field'
