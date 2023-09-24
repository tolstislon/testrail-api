import json

import responses


def test_get_user(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_user/1'),
        lambda x: (200, {}, json.dumps(
            {'email': 'testrail@ff.com', 'id': 1, 'name': 'John Smith',
             'is_active': True}
        ))
    )
    response = api.users.get_user(1)
    assert response['name'] == 'John Smith'


def test_get_user_by_email(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_user_by_email'),
        lambda x: (200, {}, json.dumps(
            {'email': x.params["email"], 'id': 1, 'name': 'John Smith',
             'is_active': True}))
    )
    email = 'testrail@cc.cc'
    response = api.users.get_user_by_email(email)
    assert response['email'] == email


def test_get_users(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_users/15'),
        lambda x: (
            200, {}, json.dumps([{'email': 'testrail@ff.com', 'id': 1,
                                  'name': 'John Smith', 'is_active': True}])
        ),
    )
    response = api.users.get_users(15)
    assert response[0]['name'] == 'John Smith'


def test_get_users_no_project_id(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_users'),
        lambda x: (
            200, {}, json.dumps([{'email': 'testrail@ff.com', 'id': 1,
                                  'name': 'John Smith', 'is_active': True}])
        ),
    )
    response = api.users.get_users()
    assert response[0]['name'] == 'John Smith'


def test_get_current_user(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_current_user/1'),
        lambda x: (
            200, {},
            json.dumps({'email': 'testrail@ff.com', 'id': 1, 'name': 'John Smith',
                        'is_active': True})
        ),
    )
    response = api.users.get_current_user(1)
    assert response['name'] == 'John Smith'
