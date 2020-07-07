import json

import responses


def post_config(r):
    data = json.loads(r.body.decode())
    return 200, {}, json.dumps({'id': 2, 'name': data['name']})


def test_get_configs(api, mock, host):
    mock.add_callback(
        responses.GET,
        '{}index.php?/api/v2/get_configs/1'.format(host),
        lambda x: (200, {}, json.dumps([{'id': 1, 'name': 'Browsers', 'configs': []}]))
    )
    resp = api.configurations.get_configs(1)
    assert resp[0]['name'] == 'Browsers'


def test_add_config_group(api, mock, host):  # no response example
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_config_group/5'.format(host),
        post_config
    )
    resp = api.configurations.add_config_group(5, name='Python')
    assert resp['name'] == 'Python'


def test_add_config(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/add_config/1'.format(host),
        post_config
    )
    resp = api.configurations.add_config(1, 'TestRail')
    assert resp['name'] == 'TestRail'


def test_update_config_group(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/update_config_group/3'.format(host),
        post_config
    )
    resp = api.configurations.update_config_group(3, 'New Name')
    assert resp['name'] == 'New Name'


def test_update_config(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/update_config/4'.format(host),
        post_config
    )
    resp = api.configurations.update_config(4, 'New config name')
    assert resp['name'] == 'New config name'


def test_delete_config_group(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_config_group/234'.format(host),
        lambda x: (200, {}, '')
    )
    resp = api.configurations.delete_config_group(234)
    assert resp is None


def test_delete_config(api, mock, host):
    mock.add_callback(
        responses.POST,
        '{}index.php?/api/v2/delete_config/54'.format(host),
        lambda x: (200, {}, '')
    )
    resp = api.configurations.delete_config(54)
    assert resp is None
