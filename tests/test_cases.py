import json
import re
from datetime import datetime
from functools import partial

import responses


def get_cases(r):
    assert r.params["suite_id"]
    assert r.params["section_id"]
    assert r.params["limit"]
    assert r.params["offset"]
    for key in "created_after", "created_before", "updated_after", "updated_before":
        assert re.match(r"^\d+$", r.params[key])
    return (
        200,
        {},
        json.dumps({"limit": 250, "offset": 250, "size": 1, "cases": [{"id": 1, "type_id": 1, "title": "My case"}]}),
    )


def add_case(r):
    data = json.loads(r.body.decode())
    return (
        200,
        {},
        json.dumps({"id": 1, "title": data["title"], "priority_id": data["priority_id"]}),
    )


def update_case(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({"id": 1, "title": data["title"]})


def update_cases(r):
    suite_id = r.url.split("/")[-1]
    data = json.loads(r.body.decode())
    return (
        200,
        {},
        json.dumps(
            {"updated": [{"id": _, "suite_id": int(suite_id), "title": data["title"]} for _ in data["case_ids"]]}
        ),
    )


def delete_cases(r, project_id=None, case_ids=None, suite_id=None, soft=0):
    assert int(r.params["soft"]) == soft
    assert int(r.params["project_id"]) == project_id
    if suite_id:
        assert f"delete_cases/{suite_id}&" in r.url
    else:
        assert "delete_cases&" in r.url
    assert json.loads(r.body.decode()) == {"case_ids": case_ids}
    return 200, {}, ""


def test_get_case(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_case/1"),
        lambda _: (200, {}, json.dumps({"id": 1, "type_id": 1, "title": "My case"})),
    )
    resp = api.cases.get_case(1)
    assert resp["id"] == 1


def test_get_cases(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_cases/1"),
        get_cases,
    )
    now = datetime.now()

    resp = api.cases.get_cases(
        1,
        suite_id=2,
        section_id=3,
        limit=5,
        offset=10,
        created_after=now,
        created_before=round(now.timestamp()),
        updated_after=now,
        updated_before=now,
    )
    assert resp.get("cases")[0]["id"] == 1


def test_add_case(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("add_case/2"),
        add_case,
    )
    resp = api.cases.add_case(2, "New case", priority_id=1)
    assert resp["title"] == "New case"
    assert resp["priority_id"] == 1


def test_update_case(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("update_case/1"),
        update_case,
    )
    resp = api.cases.update_case(1, title="New case title")
    assert resp["title"] == "New case title"


def test_delete_case(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("delete_case/5"),
        lambda _: (200, {}, ""),
    )
    resp = api.cases.delete_case(5)
    assert resp is None


def test_get_history_for_case(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_history_for_case/7"),
        lambda _: (200, {}, ""),
    )
    api.cases.get_history_for_case(7)


def test_update_cases(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("update_cases/1"),
        update_cases,
    )
    body = {"title": "New title", "estimate": "5m"}
    resp = api.cases.update_cases([1, 2, 3], 1, **body)
    assert resp["updated"][0]["title"] == "New title"
    assert resp["updated"][0]["suite_id"] == 1
    # verify [1,2,3] are the case_ids
    assert all(resp["updated"][_]["id"] in [1, 2, 3] for _ in range(len(resp["updated"])))


def test_delete_cases_no_suite_id(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("delete_cases"),
        partial(delete_cases, project_id=1, case_ids=[5, 6]),
    )
    api.cases.delete_cases(1, [5, 6])


def test_delete_cases_suite_id(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("delete_cases/1"),
        partial(delete_cases, project_id=1, suite_id=1, case_ids=[5, 6]),
    )
    api.cases.delete_cases(1, [5, 6], 1)


def test_delete_cases_suite_id_soft(api, mock, url):
    mock.add_callback(
        responses.POST,
        url("delete_cases/1"),
        partial(delete_cases, project_id=1, suite_id=1, soft=1, case_ids=[5, 6]),
    )
    api.cases.delete_cases(1, [5, 6], 1, 1)


def test_copy_cases_to_section(api, mock, url):
    mock.add_callback(responses.POST, url("copy_cases_to_section/2"), lambda x: (200, {}, x.body))
    resp = api.cases.copy_cases_to_section(section_id=2, case_ids=[1, 2, 3])
    assert resp["case_ids"] == "1,2,3"


def test_move_cases_to_section(api, mock, url):
    mock.add_callback(responses.POST, url("move_cases_to_section/5"), lambda x: (200, {}, x.body))
    resp = api.cases.move_cases_to_section(5, 6, case_ids=[1, 2, 3])
    assert resp["case_ids"] == "1,2,3"
    assert resp["suite_id"] == 6


def test_get_cases_bulk(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_cases/1"),
        get_cases,
    )
    now = datetime.now()

    resp = api.cases.get_cases_bulk(
        1,
        suite_id=2,
        section_id=3,
        limit=5,
        offset=10,
        created_after=now,
        created_before=round(now.timestamp()),
        updated_after=now,
        updated_before=now,
    )
    assert resp[0]["id"] == 1
