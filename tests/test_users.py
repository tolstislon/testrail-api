import json

import responses


def test_get_user(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_user/1'.format(host),
        lambda x: (200, {}, json.dumps(
            {'email': 'testrail@ff.com', 'id': 1, 'name': 'John Smith',
             'is_active': True}))
    )
    response = api.users.get_user(1)
    assert response['name'] == 'John Smith'


def test_get_user_by_email(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_user_by_email'.format(host),
        lambda x: (200, {}, json.dumps(
            {'email': x.params["email"], 'id': 1, 'name': 'John Smith',
             'is_active': True}))
    )
    email = 'testrail@cc.cc'
    response = api.users.get_user_by_email(email)
    assert response['email'] == email


def test_get_users(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_users/15'.format(host),
        lambda x: (
            200, {}, json.dumps([{'email': 'testrail@ff.com', 'id': 1,
                                  'name': 'John Smith', 'is_active': True}])
        ),
    )
    response = api.users.get_users(15)
    assert response[0]['name'] == 'John Smith'


def test_get_current_user(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_current_user/1'.format(host),
        lambda x: (
            200, {},
            json.dumps({'email': 'testrail@ff.com', 'id': 1, 'name': 'John Smith',
                        'is_active': True})
        ),
    )
    response = api.users.get_current_user(1)
    assert response['name'] == 'John Smith'
