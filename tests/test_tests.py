import json

import pytest
import responses


def get_tests(r):
    resp = [{"id": c, "status_id": int(i)} for c, i in enumerate(r.params["status_id"].split(","), 1)]
    return 200, {}, json.dumps({"offset": 0, "limit": 250, "size": len(resp), "tests": resp})


def test_get_test(api, mock, url):
    mock.add_callback(
        responses.GET, url("get_test/2"), lambda _: (200, {}, json.dumps({"case_id": 1, "id": 2, "run_id": 2}))
    )
    resp = api.tests.get_test(2)
    assert resp["case_id"] == 1


@pytest.mark.parametrize("status_id", ("1,5", [1, 5]))
def test_get_tests(api, mock, url, status_id):
    mock.add_callback(responses.GET, url("get_tests/2"), get_tests)
    resp = api.tests.get_tests(2, status_id=status_id).get("tests")
    assert resp[0]["status_id"] == 1
    assert resp[1]["status_id"] == 5


@pytest.mark.parametrize("status_id", ("1,5", [1, 5]))
def test_get_tests_bulk(api, mock, url, status_id):
    mock.add_callback(responses.GET, url("get_tests/2"), get_tests)
    resp = api.tests.get_tests_bulk(2, status_id=status_id)
    assert resp[0]["status_id"] == 1
    assert resp[1]["status_id"] == 5


def update_test(r):
    data = json.loads(r.body.decode())
    assert data["labels"] == [1, "smoke"]
    return 200, {}, json.dumps({"id": 2, "labels": data["labels"]})


def update_tests(r):
    data = json.loads(r.body.decode())
    assert data["test_ids"] == [2, 3]
    assert data["labels"] == [1, "smoke"]
    return 200, {}, json.dumps({"tests": data["test_ids"], "labels": data["labels"]})


def test_update_test(api, mock, url):
    mock.add_callback(responses.POST, url("update_test/2"), update_test)
    resp = api.tests.update_test(2, labels=[1, "smoke"])
    assert resp["id"] == 2
    assert resp["labels"] == [1, "smoke"]


def test_update_tests(api, mock, url):
    mock.add_callback(responses.POST, url("update_tests"), update_tests)
    resp = api.tests.update_tests([2, 3], labels=[1, "smoke"])
    assert resp["labels"] == [1, "smoke"]
