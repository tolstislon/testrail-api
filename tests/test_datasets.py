import json
import random
import uuid
from typing import Optional

import responses
from requests import PreparedRequest


def _dataset(variables_count: int = 5, dataset_id: Optional[int] = None) -> dict:
    dataset_id = dataset_id or random.randint(1, 1000)
    return {
        "id": dataset_id,
        "name": uuid.uuid4().hex,
        "variables": [
            {"id": i, "name": uuid.uuid4().hex, "value": uuid.uuid4().hex} for i in range(1, variables_count + 1)
        ],
    }


def _get_dataset(r: PreparedRequest) -> tuple[int, dict, str]:
    dataset_id = int(r.url.split("/")[-1])
    return 200, {}, json.dumps(_dataset(5, dataset_id))


def _get_datasets(_) -> tuple[int, dict, str]:
    datasets = [_dataset(variables_count=random.randint(1, 5)) for _ in range(random.randint(1, 10))]
    return (
        200,
        {},
        json.dumps(
            {
                "offset": 0,
                "limit": 250,
                "size": len(datasets),
                "_links": {"next": None, "prev": None},
                "datasets": datasets,
            }
        ),
    )


def _add_dataset(r: PreparedRequest) -> tuple[int, dict, str]:
    req = json.loads(r.body)
    variables = [{"id": i, **v} for i, v in enumerate(req["variables"], 1)]
    req["variables"] = variables
    return 200, {}, json.dumps(req)


def _update_dataset(r: PreparedRequest) -> tuple[int, dict, str]:
    req = json.loads(r.body)
    dataset_id = int(r.url.split("/")[-1])
    return (
        200,
        {},
        json.dumps(
            {
                "id": dataset_id,
                "name": req["name"],
                "variables": [{"id": i, **v} for i, v in enumerate(req["variables"], 1)],
            }
        ),
    )


def test_get_dataset(api, mock):
    dataset_id = random.randint(1, 10000)
    mock.add_callback(responses.GET, f"get_dataset/{dataset_id}", _get_dataset)
    resp = api.datasets.get_dataset(dataset_id)
    assert resp["id"] == dataset_id
    for variable in resp["variables"]:
        assert tuple(variable) == ("id", "name", "value")


def test_get_datasets(api, mock):
    project_id = random.randint(1, 1000)
    mock.add_callback(responses.GET, f"get_datasets/{project_id}", _get_datasets)
    resp = api.datasets.get_datasets(project_id)
    assert resp["size"] == len(resp["datasets"])
    for dataset in resp["datasets"]:
        assert tuple(dataset) == ("id", "name", "variables")


def test_add_dataset(api, mock):
    dataset_id, project_id = random.randint(1, 1000), random.randint(1, 1000)
    name = uuid.uuid4().hex
    variables = [{"name": uuid.uuid4().hex, "value": uuid.uuid4().hex} for _ in range(random.randint(1, 10))]
    mock.add_callback(responses.POST, f"add_dataset/{project_id}", _add_dataset)
    resp = api.datasets.add_dataset(project_id=project_id, id=dataset_id, name=name, variables=variables)
    assert resp["id"] == dataset_id
    assert resp["name"] == name
    assert len(resp["variables"]) == len(variables)


def test_update_dataset(api, mock):
    dataset_id = random.randint(1, 10000)
    mock.add_callback(responses.POST, f"update_dataset/{dataset_id}", _update_dataset)
    new_name = uuid.uuid4().hex
    variables = [{"name": uuid.uuid4().hex, "value": uuid.uuid4().hex} for _ in range(random.randint(1, 10))]
    resp = api.datasets.update_dataset(dataset_id, name=new_name, variables=variables)
    assert resp["id"] == dataset_id
    assert resp["name"] == new_name
    assert len(resp["variables"]) == len(variables)


def test_delete_dataset(api, mock):
    dataset_id = random.randint(1, 10000)
    mock.add_callback(responses.POST, f"delete_dataset/{dataset_id}", lambda _: (200, {}, None))
    resp = api.datasets.delete_dataset(dataset_id)
    assert resp is None
