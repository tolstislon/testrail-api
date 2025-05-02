import json
from functools import partial
from pathlib import Path

import pytest
import responses

from testrail_api import StatusCodeError


def add_attachment(r):
    assert "multipart/form-data" in r.headers["Content-Type"]
    assert r.headers["User-Agent"].startswith("Python TestRail API v:")
    assert r.body
    return 200, {}, json.dumps({"attachment_id": 433})


def get_attachment(_, path):
    file = Path(path, "attach.jpg")
    with file.open("rb") as f:
        return 200, {}, f


def test_add_attachment_to_plan(api, mock, url, base_path):
    mock.add_callback(responses.POST, url("add_attachment_to_plan/3"), add_attachment)
    file = Path(base_path, "attach.jpg")
    resp = api.attachments.add_attachment_to_plan(3, file)
    assert resp["attachment_id"] == 433


def test_add_attachment_to_plan_entry(api, mock, url, base_path):
    mock.add_callback(responses.POST, url("add_attachment_to_plan_entry/3/4"), add_attachment)
    file = Path(base_path, "attach.jpg")
    resp = api.attachments.add_attachment_to_plan_entry(3, 4, file)
    assert resp["attachment_id"] == 433


def test_add_attachment_to_result_pathlib(api, mock, url, base_path):
    mock.add_callback(responses.POST, url("add_attachment_to_result/2"), add_attachment)
    file = Path(base_path, "attach.jpg")
    resp = api.attachments.add_attachment_to_result(2, file)
    assert resp["attachment_id"] == 433


def test_add_attachment_to_result_str(api, mock, url, base_path):
    mock.add_callback(responses.POST, url("add_attachment_to_result/2"), add_attachment)
    file = Path(base_path, "attach.jpg")
    resp = api.attachments.add_attachment_to_result(2, str(file))
    assert resp["attachment_id"] == 433


def test_add_attachment_to_run(api, mock, url, base_path):
    mock.add_callback(method=responses.POST, url=url("add_attachment_to_run/2"), callback=add_attachment)
    file = Path(base_path, "attach.jpg")
    resp = api.attachments.add_attachment_to_run(2, file)
    assert resp["attachment_id"] == 433


def test_add_attachment_to_case_str(api, mock, url, base_path):
    mock.add_callback(responses.POST, url("add_attachment_to_case/2"), add_attachment)
    file = Path(base_path, "attach.jpg")
    resp = api.attachments.add_attachment_to_case(2, str(file))
    assert resp["attachment_id"] == 433


def test_add_attachment_to_case(api, mock, url, base_path):
    mock.add_callback(method=responses.POST, url=url("add_attachment_to_case/2"), callback=add_attachment)
    file = Path(base_path, "attach.jpg")
    resp = api.attachments.add_attachment_to_case(2, file)
    assert resp["attachment_id"] == 433


def test_get_attachments_for_case(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_case/2"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_case(2)
    assert resp.get("attachments")[0]["filename"] == "444.jpg"


def test_get_attachments_for_plan(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_plan/2"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_plan(2)
    assert resp.get("attachments")[0]["filename"] == "444.jpg"


def test_get_attachments_for_plan_entry(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_plan_entry/2/1"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_plan_entry(2, 1)
    assert resp.get("attachments")[0]["filename"] == "444.jpg"


def test_get_attachments_for_run(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_run/2"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_run(2)
    assert resp.get("attachments")[0]["filename"] == "444.jpg"


def test_get_attachments_for_test(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_test/12"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_test(12)
    assert resp.get("attachments")[0]["filename"] == "444.jpg"


def test_get_attachment(api, mock, url, base_path):
    mock.add_callback(responses.GET, url("get_attachment/433"), partial(get_attachment, path=base_path))
    file = Path(base_path, "new_attach.jpg")
    new_file = api.attachments.get_attachment(433, file)
    assert new_file.exists()
    new_file.unlink()


def test_get_attachment_str(api, mock, url, base_path):
    mock.add_callback(responses.GET, url("get_attachment/433"), partial(get_attachment, path=base_path))
    file = Path(base_path, "new_attach_str.jpg")
    new_file = api.attachments.get_attachment(433, str(file))
    assert new_file.exists()
    new_file.unlink()


def test_get_attachment_error(api, mock, url, base_path):
    mock.add_callback(responses.GET, url("get_attachment/433"), lambda _: (400, {}, ""))
    file = Path(base_path, "new_attach_str.jpg")
    with pytest.raises(StatusCodeError):
        new_file = api.attachments.get_attachment(433, str(file))
        assert new_file is None


def test_delete_attachment(api, mock, url):
    mock.add_callback(responses.POST, url("delete_attachment/433"), lambda _: (200, {}, ""))
    resp = api.attachments.delete_attachment(433)
    assert resp is None


def test_get_attachments_for_case_bulk(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_case/2"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_case_bulk(2)
    assert resp[0]["filename"] == "444.jpg"


def test_get_attachments_for_plan_bulk(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_plan/2"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_plan_bulk(2)
    assert resp[0]["filename"] == "444.jpg"


def test_get_attachments_for_run_bulk(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_run/2"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_run_bulk(2)
    assert resp[0]["filename"] == "444.jpg"


def test_get_attachments_for_plan_entry_bulk(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_plan_entry/2/1"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_plan_entry_bulk(2, 1)
    assert resp[0]["filename"] == "444.jpg"


def test_get_attachments_for_test_bulk(api, mock, url):
    mock.add_callback(
        responses.GET,
        url("get_attachments_for_test/2"),
        lambda _: (
            200,
            {},
            json.dumps({"limit": 250, "offset": 250, "size": 1, "attachments": [{"id": 1, "filename": "444.jpg"}]}),
        ),
    )
    resp = api.attachments.get_attachments_for_test_bulk(2)
    assert resp[0]["filename"] == "444.jpg"
