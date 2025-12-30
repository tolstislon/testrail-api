import json

import pytest
import responses


def get_users(req):
    return (
        200,
        {},
        json.dumps(
            {
                "offset": int(req.params.get("offset", 0)),
                "limit": int(req.params.get("limit", 250)),
                "size": 2,
                "users": [
                    {"email": "testrail@ff.com", "id": 1, "name": "John Smith", "is_active": True},
                    {"email": "testrail1@ff.com", "id": 2, "name": "Jane Smith", "is_active": True},
                ],
            }
        ),
    )


def test_get_user(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_user/1"),
        lambda _: (200, {}, json.dumps({"email": "testrail@ff.com", "id": 1, "name": "John Smith", "is_active": True})),
    )
    response = api.users.get_user(1)
    assert response["name"] == "John Smith"


def test_get_user_by_email(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_user_by_email"),
        lambda x: (200, {}, json.dumps({"email": x.params["email"], "id": 1, "name": "John Smith", "is_active": True})),
    )
    email = "testrail@cc.cc"
    response = api.users.get_user_by_email(email)
    assert response["email"] == email


@pytest.mark.parametrize(("offset", "limit"), ((None, None), (0, 250), (2, 14)))
def test_get_users(api, mock, url, offset, limit):
    mock.add_callback(responses.GET, url("get_users/15"), get_users)
    response = api.users.get_users(15, offset=offset, limit=limit)
    assert response["offset"] == (offset if offset is not None else 0)
    assert response["limit"] == (limit if limit is not None else 250)
    assert response["users"][0]["name"] == "John Smith"


@pytest.mark.parametrize(("offset", "limit"), ((None, None), (0, 250), (2, 14)))
def test_get_users_no_project_id(api, mock, url, offset, limit):
    mock.add_callback(responses.GET, url("get_users"), get_users)
    response = api.users.get_users(offset=offset, limit=limit)
    assert response["offset"] == (offset if offset is not None else 0)
    assert response["limit"] == (limit if limit is not None else 250)
    assert response["users"][0]["name"] == "John Smith"


def test_get_current_user(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_current_user/1"),
        lambda _: (200, {}, json.dumps({"email": "testrail@ff.com", "id": 1, "name": "John Smith", "is_active": True})),
    )
    response = api.users.get_current_user(1)
    assert response["name"] == "John Smith"
