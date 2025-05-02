import functools
import json
import re
from datetime import datetime

import pytest
import responses


def get_results(r, limit="3"):
    assert r.params["limit"] == limit
    assert r.params["status_id"] == "1,2,3"
    return (
        200,
        {},
        json.dumps({"offset": 0, "limit": 250, "size": 1, "results": [{"id": 1, "status_id": 2, "test_id": 1}]}),
    )


def get_results_for_run(r, limit="3"):
    assert r.params["limit"] == limit
    assert r.params["status_id"] == "1,2,3"
    for key in "created_after", "created_before":
        assert re.match(r"^\d+$", r.params[key])
    return (
        200,
        {},
        json.dumps({"offset": 0, "limit": 250, "size": 1, "results": [{"id": 1, "status_id": 2, "test_id": 1}]}),
    )


def add_result(r):
    data = json.loads(r.body.decode())
    return (
        200,
        {},
        json.dumps(
            {
                "id": 1,
                "status_id": data["status_id"],
                "test_id": 15,
                "assignedto_id": data["assignedto_id"],
                "comment": data["comment"],
            }
        ),
    )


def add_results(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps(data["results"])


@pytest.mark.parametrize("status_id", ("1,2,3", [1, 2, 3]))
def test_get_results(api, mock, url, status_id):
    mock.add_callback(responses.GET, url("get_results/221"), get_results)
    resp = api.results.get_results(221, limit=3, status_id=status_id).get("results")
    assert resp[0]["status_id"] == 2


@pytest.mark.parametrize("status_id", ("1,2,3", [1, 2, 3]))
def test_get_results_for_case(api, mock, url, status_id):
    mock.add_callback(responses.GET, url("get_results_for_case/23/2567"), get_results)
    resp = api.results.get_results_for_case(23, 2567, limit=3, status_id=status_id).get("results")
    assert resp[0]["status_id"] == 2


@pytest.mark.parametrize("status_id", ("1,2,3", [1, 2, 3]))
def test_get_results_for_run(api, mock, url, status_id):
    mock.add_callback(responses.GET, url("get_results_for_run/12"), get_results_for_run)
    resp = api.results.get_results_for_run(
        12, limit=3, status_id=status_id, created_after=datetime.now(), created_before=datetime.now()
    ).get("results")
    assert resp[0]["status_id"] == 2


def test_add_result(api, mock, url):
    mock.add_callback(responses.POST, url("add_result/15"), add_result)
    resp = api.results.add_result(15, status_id=5, comment="Fail", assignedto_id=1)
    assert resp["status_id"] == 5
    assert resp["comment"] == "Fail"
    assert resp["assignedto_id"] == 1


def test_add_result_for_case(api, mock, url):
    mock.add_callback(responses.POST, url("add_result_for_case/3/34"), add_result)
    resp = api.results.add_result_for_case(3, 34, status_id=1, comment="Passed", assignedto_id=1)
    assert resp["status_id"] == 1
    assert resp["comment"] == "Passed"
    assert resp["assignedto_id"] == 1


def test_add_results(api, mock, url):
    mock.add_callback(responses.POST, url("add_results/15"), add_results)
    results = [{"test_id": 1, "status_id": 5}, {"test_id": 2, "status_id": 1}]
    resp = api.results.add_results(15, results=results)
    assert resp == results


def test_add_results_for_cases(api, mock, url):
    mock.add_callback(responses.POST, url("add_results_for_cases/18"), add_results)
    results = [{"case_id": 1, "status_id": 5}, {"case_id": 2, "status_id": 1}]
    resp = api.results.add_results_for_cases(18, results)
    assert resp == results


@pytest.mark.parametrize("status_id", ("1,2,3", [1, 2, 3]))
def test_get_results_bulk(api, mock, url, status_id):
    get_results_bulk = functools.partial(get_results, limit="250")
    mock.add_callback(responses.GET, url("get_results/221"), get_results_bulk)
    resp = api.results.get_results_bulk(221, status_id=status_id)
    assert resp[0]["status_id"] == 2


@pytest.mark.parametrize("status_id", ("1,2,3", [1, 2, 3]))
def test_get_results_for_case_bulk(api, mock, url, status_id):
    get_results_for_case_bulk = functools.partial(get_results, limit="250")
    mock.add_callback(
        responses.GET,
        url("get_results_for_case/23/2567"),
        get_results_for_case_bulk,
    )
    resp = api.results.get_results_for_case_bulk(23, 2567, status_id=status_id)
    assert resp[0]["status_id"] == 2


@pytest.mark.parametrize("status_id", ("1,2,3", [1, 2, 3]))
def test_get_results_for_run_bulk(api, mock, url, status_id):
    get_results_for_run_bulk = functools.partial(get_results_for_run, limit="250")
    mock.add_callback(responses.GET, url("get_results_for_run/12"), get_results_for_run_bulk)
    resp = api.results.get_results_for_run_bulk(
        12, status_id=status_id, created_after=datetime.now(), created_before=datetime.now()
    )
    assert resp[0]["status_id"] == 2
