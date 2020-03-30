import random
import string as st
from datetime import datetime

import pytest
from requests.exceptions import ConnectTimeout

from testrail_api import StatusCodeError


def random_string():
    return ''.join(random.sample(st.ascii_lowercase, 10))


def test_users(api):
    all_users = api.users.get_users()
    this_user, *_ = [i for i in all_users if i['email'] == api.user_email]
    assert this_user

    user = api.users.get_user(this_user['id'])
    assert this_user == user

    response = api.users.get_user_by_email(api.user_email)
    assert response['email'] == api.user_email


def test_project(api):
    new_project = api.projects.add_project(
        name=datetime.now().isoformat(),
        announcement='test',
        show_announcement=True,
        suite_mode=1
    )
    projects = api.projects.get_projects()
    assert [i for i in projects if i['id'] == new_project['id']]
    this_project = api.projects.get_project(new_project['id'])
    assert this_project == new_project

    updated_project = api.projects.update_project(new_project['id'], is_completed=True)
    assert updated_project['is_completed'] is True

    response = api.projects.get_projects(is_completed=1)
    assert [i for i in response if i['id'] == new_project['id']]

    api.projects.delete_project(new_project['id'])


def test_suites(suites_project):
    api, project_id = suites_project
    suite = api.suites.add_suite(project_id, 'new_suite', description='test')

    suites = api.suites.get_suites(project_id)
    assert [i for i in suites if i['id'] == suite['id']]
    new_name, new_description = 'new_suite2', 'test2'
    api.suites.update_suite(suite['id'], name=new_name, description=new_description)

    r = api.suites.get_suite(suite['id'])
    assert r['name'] == new_name and r['description'] == new_description
    api.suites.delete_suite(suite['id'])


def test_milestones(suites_project):
    api, project_id = suites_project
    milestone = api.milestones.add_milestone(
        project_id,
        datetime.now().isoformat(),
        start_on=int(datetime.now().timestamp())
    )
    milestones = api.milestones.get_milestones(project_id)
    assert [i for i in milestones if i['id'] == milestone['id']]

    api.milestones.update_milestone(milestone['id'], is_completed=True)

    r = api.milestones.get_milestone(milestone['id'])
    assert r['is_completed'] is True

    api.milestones.delete_milestone(milestone['id'])


def test_templates(default_project):
    api, project_id = default_project
    api.templates.get_templates(project_id)


def test_sections(default_project):
    api, project_id = default_project
    section = api.sections.add_section(project_id, 'test')

    sections = api.sections.get_sections(project_id)
    assert [i for i in sections if i['id'] == section['id']]

    new_name = 'test2'
    api.sections.update_section(section['id'], name=new_name)

    r = api.sections.get_section(section['id'])
    assert r['name'] == new_name

    api.sections.delete_section(section['id'])


def test_case_fields(api):
    case_field = api.case_fields.add_case_field(
        'String',
        random_string(),
        random_string(),
        include_all=True,
        configs=[{
            "context": {"is_global": True, "project_ids": [1]},
            "options": {"is_required": False, "items": "1, One\n2, Two"}
        }]
    )
    fields = api.case_fields.get_case_fields()
    assert [i for i in fields if i['id'] == case_field['id']]


def test_case_types(api):
    api.case_types.get_case_types()


def test_configurations(default_project):
    api, project_id = default_project
    config_group = api.configurations.post_config(project_id, 'config_group')
    config = api.configurations.add_config(config_group['id'], 'config')

    api.configurations.update_config(config['id'], 'config2')
    api.configurations.update_config_group(config_group['id'], 'config_group2')

    api.configurations.get_configs(project_id)

    api.configurations.delete_config(config['id'])
    api.configurations.delete_config_group(config_group['id'])

    with pytest.raises(StatusCodeError):
        api.configurations.delete_config_group(config_group['id'])


def test_result_fields(api):
    api.result_fields.get_result_fields()


def test_cases(default_project):
    api, project_id = default_project
    r = api.sections.add_section(project_id, 'test')
    sections_id = r['id']
    r = api.case_types.get_case_types()
    type_id = random.choice(r)['id']
    r = api.priorities.get_priorities()
    priority_id = random.choice(r)['id']

    r = api.cases.add_case(
        sections_id,
        datetime.now().isoformat(),
        template_id=1,
        type_id=type_id,
        priority_id=priority_id,
        custom_mission='qwe',
        custom_goals='qwe1',
    )
    case_id = r['id']

    r = api.cases.get_cases(project_id)
    assert len(r) == 1
    estimate = '5m'
    api.cases.update_case(case_id, estimate=estimate)
    r = api.cases.get_case(case_id)
    assert r['id'] == case_id and r['estimate'] == estimate
    api.cases.delete_case(case_id)


def test_statuses(api):
    api.statuses.get_statuses()


def test_plan(suites_project):
    api, project_id = suites_project
    r = api.suites.add_suite(project_id, 'new_suite')
    suite_id = r['id']
    r = api.plans.add_plan(project_id, 'test_plan', entries=[{"suite_id": suite_id, "name": "Run", }])
    plan_id = r['id']
    r = api.plans.get_plans(project_id)
    assert len(r) == 1
    description = 'test_plan_description'
    api.plans.update_plan(plan_id, description=description)
    r = api.plans.get_plan(plan_id)
    assert r['id'] == plan_id and r['description'] == description
    r = api.plans.add_plan_entry(plan_id, suite_id, name='plan_entry')
    entry_id = r['id']
    api.plans.update_plan_entry(plan_id, entry_id, description=description)
    api.plans.delete_plan_entry(plan_id, entry_id)
    api.plans.delete_plan(plan_id)
    r = api.plans.add_plan(project_id, 'test_plan2')
    plan_id = r['id']
    api.plans.close_plan(plan_id)


def test_runs(default_project):
    api, project_id = default_project
    r = api.runs.add_run(project_id)
    run_id = r['id']
    r = api.runs.get_runs(project_id)
    assert len(r) == 1
    name = 'update name'
    api.runs.update_run(run_id, name=name)
    r = api.runs.get_run(run_id)
    assert r['id'] == run_id, r['name'] == name
    api.runs.delete_run(run_id)
    r = api.runs.add_run(project_id)
    run_id = r['id']
    api.runs.close_run(run_id)


def test_results_and_tests(default_project_case):
    api, project_id, case_ids = default_project_case
    r = api.runs.add_run(project_id, case_ids=case_ids)
    run_id = r['id']

    for i in case_ids:
        api.results.add_result_for_case(run_id, i, status_id=1, comment='pass', version='1')
    r = api.results.get_results_for_case(run_id, random.choice(case_ids))
    assert len(r) == 1
    data = [{'case_id': i, 'status_id': 2, 'comment': 'Blocked'} for i in case_ids]
    api.results.add_results_for_cases(run_id, data)
    api.results.get_results_for_run(run_id)

    r = api.tests.get_tests(run_id)
    test_ids = [i['id'] for i in r]
    test_id = random.choice(test_ids)
    api.tests.get_test(test_id)
    api.results.add_result(test_id, status_id=1, comment='pass', version='1')
    api.results.get_results(test_id)
    data = [{'test_id': i, 'status_id': 2, 'comment': 'Blocked'} for i in test_ids]
    api.results.add_results(run_id, data)


def test_attachments(default_project_case):
    api, project_id, case_ids = default_project_case
    r = api.runs.add_run(project_id, case_ids=case_ids)
    run_id = r['id']
    case_id = random.choice(case_ids)
    r = api.results.add_result_for_case(run_id, case_id, status_id=1, comment='pass', version='1')
    result_id, test_id = r['id'], r['test_id']
    r = api.attachments.add_attachment_to_result(result_id, './tests/real/attach.jpg')
    attachment_id = r['attachment_id']
    api.attachments.get_attachments_for_case(case_id)
    api.attachments.get_attachments_for_test(test_id)
    file = api.attachments.get_attachment(attachment_id, './tests/real/new_attach.jpg')
    file.unlink()
    api.attachments.delete_attachment(attachment_id)
    with pytest.raises(StatusCodeError):
        api.attachments.get_attachment(attachment_id, '')


def test_negative(time_out_api):
    api = time_out_api
    with pytest.raises(ConnectTimeout):
        api.projects.get_projects()
    with pytest.warns(DeprecationWarning):
        api.attachments.add_attachment_to_result_for_case(1, 2, '.')
