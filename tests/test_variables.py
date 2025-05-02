import json
import random
import uuid

import responses
from requests import PreparedRequest


def _add_variables(r: PreparedRequest) -> tuple[int, dict, str]:
    req = json.loads(r.body)
    assert "id" in req and "name" in req
    return 200, {}, json.dumps(req)


def _update_variable(r: PreparedRequest) -> tuple[int, dict, str]:
    req = json.loads(r.body)
    v = r.url.split("/")[-1]
    return 200, {}, json.dumps({"id": int(v), "name": req["name"]})


def test_get_variables(api, mock, url):
    project_id = random.randint(1, 10000)
    mock.add_callback(
        responses.GET,
        url(f"get_variables/{project_id}"),
        lambda _: (
            200,
            {},
            json.dumps(
                {
                    "offset": 0,
                    "limit": 250,
                    "size": 2,
                    "_links": {"next": None, "prev": None},
                    "variables": [{"id": 611, "name": "d"}, {"id": 612, "name": "e"}],
                }
            ),
        ),
    )
    response = api.variables.get_variables(project_id)
    assert response["size"] == 2
    for variable in response["variables"]:
        assert tuple(variable) == ("id", "name")


def test_add_variables(api, mock, url):
    project_id = random.randint(1, 10000)
    _id, _name = random.randint(1, 10000), uuid.uuid4().hex
    mock.add_callback(responses.POST, url(f"add_variable/{project_id}"), _add_variables)
    response = api.variables.add_variable(project_id, _id, _name)
    assert response["id"] == _id
    assert response["name"] == _name


def test_update_variable(api, mock, url):
    variable_id = random.randint(1, 10000)
    _name = uuid.uuid4().hex
    mock.add_callback(responses.POST, url(f"update_variable/{variable_id}"), _update_variable)
    response = api.variables.update_variable(variable_id=variable_id, name=_name)
    assert response["id"] == variable_id
    assert response["name"] == _name


def test_delete_variable(api, mock, url):
    variable_id = random.randint(1, 10000)
    mock.add_callback(responses.POST, url(f"delete_variable/{variable_id}"), lambda _: (200, {}, None))
    response = api.variables.delete_variable(variable_id)
    assert response is None
