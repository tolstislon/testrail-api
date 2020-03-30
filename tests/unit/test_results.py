import json

import responses


def get_results(r):
    assert r.params['limit'] == '3'
    assert r.params['status_id'] == '1,2,3'
    return 200, {}, json.dumps([{'id': 1, 'status_id': 2, 'test_id': 1}])


def add_result(r):
    data = json.loads(r.body)
    return 200, {}, json.dumps(
        {'id': 1, 'status_id': data['status_id'], 'test_id': 15, 'assignedto_id': data['assignedto_id'],
         'comment': data['comment']}
    )


def add_results(r):
    data = json.loads(r.body)
    return 200, {}, json.dumps(data['results'])


def test_get_results(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_results/221',
        get_results
    )
    resp = api.results.get_results(221, limit=3, status_id='1,2,3')
    assert resp[0]['status_id'] == 2


def test_get_results_for_case(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_results_for_case/23/2567',
        get_results
    )
    resp = api.results.get_results_for_case(23, 2567, limit=3, status_id='1,2,3')
    assert resp[0]['status_id'] == 2


def test_get_results_for_run(api, mock, host):
    mock.add_callback(
        responses.GET,
        f'{host}index.php?/api/v2/get_results_for_run/12',
        get_results
    )
    resp = api.results.get_results_for_run(12, limit=3, status_id='1,2,3')
    assert resp[0]['status_id'] == 2


def test_add_result(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/add_result/15',
        add_result
    )
    resp = api.results.add_result(15, status_id=5, comment='Fail', assignedto_id=1)
    assert resp['status_id'] == 5
    assert resp['comment'] == 'Fail'
    assert resp['assignedto_id'] == 1


def test_add_result_for_case(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/add_result_for_case/3/34',
        add_result
    )
    resp = api.results.add_result_for_case(3, 34, status_id=1, comment='Passed', assignedto_id=1)
    assert resp['status_id'] == 1
    assert resp['comment'] == 'Passed'
    assert resp['assignedto_id'] == 1


def test_add_results(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/add_results/15',
        add_results
    )
    results = [{'test_id': 1, 'status_id': 5}, {'test_id': 2, 'status_id': 1}]
    resp = api.results.add_results(12, results=results)
    assert resp == results


def test_add_results_for_cases(api, mock, host):
    mock.add_callback(
        responses.POST,
        f'{host}index.php?/api/v2/add_results_for_cases/18',
        add_results
    )
    results = [{'case_id': 1, 'status_id': 5}, {'case_id': 2, 'status_id': 1}]
    resp = api.results.add_results_for_cases(18, results)
    assert resp == results
