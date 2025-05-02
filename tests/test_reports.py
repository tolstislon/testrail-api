import json

import responses


def test_get_reports(api, mock, url):
    project_id = 1
    mock.add_callback(
        responses.GET,
        url(f"get_reports/{project_id}"),
        lambda _: (200, {}, json.dumps([{"id": 1, "name": "Activity Summary"}])),
    )
    response = api.reports.get_reports(project_id)
    assert response[0]["name"] == "Activity Summary"


def test_run_report(api, mock, url):
    report_url, report_template_id = "https://...383", 1
    mock.add_callback(
        responses.GET,
        url(f"run_report/{report_template_id}"),
        lambda _: (200, {}, json.dumps({"report_url": report_url})),
    )
    response = api.reports.run_report(report_template_id)
    assert response["report_url"] == report_url
