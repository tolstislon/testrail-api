import json

import responses


def test_get_reports(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('get_reports/1'),
        lambda x: (200, {}, json.dumps([{'id': 1, 'name': 'Activity Summary'}]))
    )
    response = api.reports.get_reports(1)
    assert response[0]['name'] == 'Activity Summary'


def test_run_report(api, mock, url):
    mock.add_callback(
        responses.GET,
        url('run_report/1'),
        lambda x: (200, {}, json.dumps({'report_url': 'https://...383'}))
    )
    response = api.reports.run_report(1)
    assert response['report_url'] == 'https://...383'
