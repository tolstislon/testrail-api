import json
from functools import partial
from pathlib import Path

import pytest
import responses

from testrail_api import StatusCodeError


def add_attachment(r):
    assert 'multipart/form-data' in r.headers['Content-Type']
    assert r.headers['User-Agent'].startswith('Python TestRail API v:')
    assert r.body
    return 200, {}, json.dumps({'attachment_id': 433})


def get_attachment(r, path):
    file = Path(path, 'attach.jpg')
    with file.open('rb') as f:
        return 200, {}, f


def test_add_attachment_to_result_pathlib(api, mock, host, base_path):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_attachment_to_result/2'.format(host),
        add_attachment
    )
    file = Path(base_path, 'attach.jpg')
    resp = api.attachments.add_attachment_to_result(2, file)
    assert resp['attachment_id'] == 433


def test_add_attachment_to_result_str(api, mock, host, base_path):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_attachment_to_result/2'.format(host),
        add_attachment
    )
    file = Path(base_path, 'attach.jpg')
    resp = api.attachments.add_attachment_to_result(2, str(file))
    assert resp['attachment_id'] == 433


def test_get_attachments_for_case(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_attachments_for_case/2'.format(host),
        lambda x: (200, {}, json.dumps([{'id': 1, 'filename': '444.jpg'}]))
    )
    resp = api.attachments.get_attachments_for_case(2)
    assert resp[0]['filename'] == '444.jpg'


def test_get_attachments_for_test(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_attachments_for_test/12'.format(host),
        lambda x: (200, {}, json.dumps([{'id': 1, 'filename': '444.jpg'}]))
    )
    resp = api.attachments.get_attachments_for_test(12)
    assert resp[0]['filename'] == '444.jpg'


def test_get_attachment(api, mock, host, base_path):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_attachment/433'.format(host),
        partial(get_attachment, path=base_path)
    )
    file = Path(base_path, 'new_attach.jpg')
    new_file = api.attachments.get_attachment(433, file)
    assert new_file.exists()
    new_file.unlink()


def test_get_attachment_str(api, mock, host, base_path):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_attachment/433'.format(host),
        partial(get_attachment, path=base_path)
    )
    file = Path(base_path, 'new_attach_str.jpg')
    new_file = api.attachments.get_attachment(433, str(file))
    assert new_file.exists()
    new_file.unlink()


def test_get_attachment_error(api, mock, host, base_path):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_attachment/433'.format(host),
        lambda x: (400, {}, '')
    )
    file = Path(base_path, 'new_attach_str.jpg')
    with pytest.raises(StatusCodeError):
        new_file = api.attachments.get_attachment(433, str(file))
        assert new_file is None


def test_delete_attachment(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_attachment/433'.format(host),
        lambda x: (200, {}, '')
    )
    resp = api.attachments.delete_attachment(433)
    assert resp is None
