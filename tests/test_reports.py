import json

import responses


def test_get_reports(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_reports/1'.format(host),
        lambda x: (200, {}, json.dumps([{'id': 1, 'name': 'Activity Summary'}]))
    )
    response = api.reports.get_reports(1)
    assert response[0]['name'] == 'Activity Summary'


def test_run_report(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/run_report/1'.format(host),
        lambda x: (200, {}, json.dumps({'report_url': 'https://...383'}))
    )
    response = api.reports.run_report(1)
    assert response['report_url'] == 'https://...383'
