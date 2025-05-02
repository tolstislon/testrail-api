import json

import responses


def get_roles(_):
    return (
        200,
        {},
        json.dumps(
            {
                "offset": 0,
                "limit": 250,
                "size": 1,
                "roles": [
                    {"id": 3, "name": "Tester", "is_default": False, "is_project_admin": False},
                    {"id": 1, "name": "Lead", "is_default": True, "is_project_admin": False},
                ],
            }
        ),
    )


def test_get_roles(api, mock, url):
    mock.add_callback(responses.GET, url("get_roles"), get_roles)
    resp = api.roles.get_roles()
    assert resp["roles"][1]["name"] == "Lead"
