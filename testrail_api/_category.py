"""
TestRail API categories
"""

import warnings
from pathlib import Path
from typing import List, Optional, Union

from ._enums import METHODS


class BaseCategory:

    def __init__(self, session):
        self._session = session


class Cases(BaseCategory):

    def get_case(self, case_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-cases#get_case

        Returns an existing test case.
        :param case_id: The ID of the test case
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_case/{case_id}')

    def get_cases(self, project_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-cases#get_cases

        Returns a list of test cases for a test suite or specific section in a test suite.
        :param project_id: The ID of the project
            :key suite_id: int - The ID of the test suite (optional if the project is operating in single suite mode)
            :key section_id: int - The ID of the section (optional)
            :key limit: int - The number of test cases the response should return
            :key offset: Where to start counting the tests cases from (the offset)
            :key filter: Only return cases with matching filter string in the case title
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_cases/{project_id}', params=kwargs)

    def add_case(self, section_id: int, title: str, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-cases#add_case

        Creates a new test case.
        :param section_id: The ID of the section the test case should be added to
        :param title: The title of the test case (required)
            :key template_id: int - The ID of the template (field layout) (requires TestRail 5.2 or later)
            :key type_id: int - The ID of the case type
            :key priority_id: int - The ID of the case priority
            :key estimate: str - The estimate, e.g. "30s" or "1m 45s"
            :key milestone_id: int - The ID of the milestone to link to the test case
            :key refs: str - A comma-separated list of references/requirements

        Custom fields are supported as well and must be submitted with their system name, prefixed with 'custom_', e.g.:
        {
            ..
            "custom_preconds": "These are the preconditions for a test case"
            ..
        }
        :return: response
        """
        data = dict(title=title, **kwargs)
        return self._session.request(METHODS.POST, f'add_case/{section_id}', json=data)

    def update_case(self, case_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-cases#update_case

        Updates an existing test case (partial updates are supported, i.e.
        you can submit and update specific fields only).
        :param case_id: The ID of the test case
        :param kwargs: This method supports the same POST fields as add_case (except section_id).
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_case/{case_id}', json=kwargs)

    def delete_case(self, case_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-cases#delete_case

        Deletes an existing test case.
        :param case_id: The ID of the test case
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_case/{case_id}')


class CaseFields(BaseCategory):

    def get_case_fields(self) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-cases-fields#get_case_fields

        Returns a list of available test case custom fields.
        :return: response
        """
        return self._session.request(METHODS.GET, 'get_case_fields')

    def add_case_field(self, type: str, name: str, label: str, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-cases-fields#add_case_field

        Creates a new test case custom field.
        :param type: str - The type identifier for the new custom field (required). The following types are supported:
                    String, Integer, Text, URL, Checkbox, Dropdown, User, Date, Milestone, Steps, Multiselect
                    You can pass the number of the type as well as the word, e.g. "5", "string", "String", "Dropdown",
                    "12". The numbers must be sent as a string e.g {type: "5"} not {type: 5},
                    otherwise you will get a 400 (Bad Request) response.
        :param name: str - The name for new the custom field (required)
        :param label: str - The label for the new custom field (required)
            :key description: str - The description for the new custom field
            :key include_all: bool - Set flag to true if you want the new custom field included for all templates.
                                    Otherwise (false) specify the ID's of templates to be included as the next
                                    parameter (template_ids)
            :key template_ids: list - ID's of templates new custom field will apply to if include_all is set to false
            :key configs: dict - An object wrapped in an array with two default keys, 'context' and 'options'
        :return: response
        """
        data = dict(type=type, name=name, label=label, **kwargs)
        return self._session.request(METHODS.POST, 'add_case_field', json=data)


class CaseTypes(BaseCategory):

    def get_case_types(self) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-cases-types#get_case_types

        Returns a list of available case types.
        :return: response
        """
        return self._session.request(METHODS.GET, 'get_case_types')


class Configurations(BaseCategory):

    def get_configs(self, project_id: int) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-configs#get_configs

        Returns a list of available configurations, grouped by configuration groups (requires TestRail 3.1 or later).
        :param project_id: The ID of the project
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_configs/{project_id}')

    def add_config_group(self, project_id: int, name: str) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-configs#add_config_group

        Creates a new configuration group (requires TestRail 5.2 or later).
        :param project_id: The ID of the project the configuration group should be added to
        :param name: The name of the configuration group (required)
        :return: response
        """
        return self._session.request(METHODS.POST, f'add_config_group/{project_id}', json={'name': name})

    def add_config(self, config_group_id: int, name: str) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-configs#add_config

        Creates a new configuration (requires TestRail 5.2 or later).
        :param config_group_id: The ID of the configuration group the configuration should be added to
        :param name: The name of the configuration (required)
        :return: response
        """
        return self._session.request(METHODS.POST, f'add_config/{config_group_id}', json={'name': name})

    def update_config_group(self, config_group_id: int, name: str) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-configs#update_config_group

        Updates an existing configuration group (requires TestRail 5.2 or later).
        :param config_group_id: The ID of the configuration group
        :param name: The name of the configuration group
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_config_group/{config_group_id}', json={'name': name})

    def update_config(self, config_id: int, name: str) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-configs#update_config

        Updates an existing configuration (requires TestRail 5.2 or later).
        :param config_id: The ID of the configuration
        :param name: The name of the configuration
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_config/{config_id}', json={'name': name})

    def delete_config_group(self, config_group_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-configs#delete_config_group

        Deletes an existing configuration group and its configurations (requires TestRail 5.2 or later).
        :param config_group_id: The ID of the configuration group
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_config_group/{config_group_id}')

    def delete_config(self, config_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-configs#delete_config

        Deletes an existing configuration (requires TestRail 5.2 or later).
        :param config_id: The ID of the configuration
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_config/{config_id}')


class Milestones(BaseCategory):

    def get_milestone(self, milestone_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-milestones#get_milestone

        Returns an existing milestone.
        :param milestone_id: The ID of the milestone
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_milestone/{milestone_id}')

    def get_milestones(self, project_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-milestones#get_milestones

        Returns the list of milestones for a project.
        :param project_id: The ID of the project
            :key is_completed: 1 to return completed milestones only. 0 to return open (active/upcoming)
                                 milestones only (available since TestRail 4.0).
            :key is_started: 1 to return started milestones only. 0 to return upcoming milestones only
                                (available since TestRail 5.3).
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_milestones/{project_id}', params=kwargs)

    def add_milestone(self, project_id: int, name: str, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-milestones#add_milestone

        Creates a new milestone.
        :param project_id: 	The ID of the project the milestone should be added to
        :param name: str - The name of the milestone (required)

            :key description: str - The description of the milestone
            :key due_on: int - The due date of the milestone (as UNIX timestamp)
            :key parent_id: int - The ID of the parent milestone, if any (for sub-milestones)
                                        (available since TestRail 5.3)
            :key start_on: int - The scheduled start date of the milestone (as UNIX timestamp)
                                    (available since TestRail 5.3)
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(METHODS.POST, f'add_milestone/{project_id}', json=data)

    def update_milestone(self, milestone_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-milestones#update_milestone

        Updates an existing milestone (partial updates are supported, i.e.
        you can submit and update specific fields only).
        :param milestone_id: The ID of the milestone
            :key is_completed: bool - True if a milestone is considered completed and false otherwise
            :key is_started: bool - True if a milestone is considered started and false otherwise
            :key parent_id: int - The ID of the parent milestone, if any (for sub-milestones)
                                                    (available since TestRail 5.3)
            :key start_on: int - The scheduled start date of the milestone (as UNIX timestamp)
                                                    (available since TestRail 5.3)
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_milestone/{milestone_id}', json=kwargs)

    def delete_milestone(self, milestone_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-milestones#delete_milestone

        Deletes an existing milestone.
        :param milestone_id: The ID of the milestone
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_milestone/{milestone_id}')


class Plans(BaseCategory):

    def get_plan(self, plan_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#get_plan

        Returns an existing test plan.
        :param plan_id: The ID of the test plan
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_plan/{plan_id}')

    def get_plans(self, project_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#get_plans

        Returns a list of test plans for a project.
        :param project_id: The ID of the project
        :param kwargs: filters
            :key created_after: int - Only return test plans created after this date (as UNIX timestamp).
            :key created_before: int - Only return test plans created before this date (as UNIX timestamp).
            :key created_by: int(list) - A comma-separated list of creators (user IDs) to filter by.
            :key is_completed: int - 1 to return completed test plans only. 0 to return active test plans only.
            :key limit/offset: int - Limit the result to :limit test plans. Use :offset to skip records.
            :key milestone_id: int(list) - A comma-separated list of milestone IDs to filter by.
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_plans/{project_id}', params=kwargs)

    def add_plan(self, project_id: int, name: str, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#add_plan

        Creates a new test plan.
        :param project_id: The ID of the project the test plan should be added to
        :param name: The name of the test plan (required)
            :key description: str - The description of the test plan
            :key milestone_id: int - The ID of the milestone to link to the test plan
            :key entries: list - An array of objects describing the test runs of the plan,
                                see the example below and add_plan_entry
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(METHODS.POST, f'add_plan/{project_id}', json=data)

    def add_plan_entry(self, plan_id: int, suite_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#add_plan_entry

        Adds one or more new test runs to a test plan.
        :param plan_id: The ID of the plan the test runs should be added to
        :param suite_id: The ID of the test suite for the test run(s) (required)
            :key name: str - The name of the test run(s)
            :key description: str - The description of the test run(s) (requires TestRail 5.2 or later)
            :key assignedto_id: int - The ID of the user the test run(s) should be assigned to
            :key include_all: bool - True for including all test cases of the test suite and false for a custom case
                                        selection (default: true)
            :key case_ids: list - An array of case IDs for the custom case selection
            :key config_ids: list - An array of configuration IDs used for the test runs of the test plan entry
                                            (requires TestRail 3.1 or later)
            :key runs: list - An array of test runs with configurations, please see the example below for details
                                (requires TestRail 3.1 or later)
        :return: response
        """
        data = dict(suite_id=suite_id, **kwargs)
        return self._session.request(METHODS.POST, f'add_plan_entry/{plan_id}', json=data)

    def update_plan(self, plan_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#update_plan

        Updates an existing test plan (partial updates are supported,
        i.e. you can submit and update specific fields only).
        :param plan_id: The ID of the test plan
        :param kwargs: With the exception of the entries field, this method supports the same POST fields as add_plan.
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_plan/{plan_id}', json=kwargs)

    def update_plan_entry(self, plan_id: int, entry_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#update_plan_entry

        Updates one or more existing test runs in a plan (partial updates are supported,
        i.e. you can submit and update specific fields only).
        :param plan_id: The ID of the test plan
        :param entry_id: The ID of the test plan entry (note: not the test run ID)
            :key name: str - The name of the test run(s)
            :key description: str - The description of the test run(s) (requires TestRail 5.2 or later)
            :key assignedto_id: int - The ID of the user the test run(s) should be assigned to
            :key include_all: bool - True for including all test cases of the test suite and false for a custom case
                                    selection (default: true)
            :key case_ids: list - An array of case IDs for the custom case selection
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_plan_entry/{plan_id}/{entry_id}', json=kwargs)

    def close_plan(self, plan_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#close_plan

        Closes an existing test plan and archives its test runs & results.
        :param plan_id: The ID of the test plan
        :return: response
        """
        return self._session.request(METHODS.POST, f'close_plan/{plan_id}')

    def delete_plan(self, plan_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#delete_plan

        Deletes an existing test plan.
        :param plan_id: The ID of the test plan
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_plan/{plan_id}')

    def delete_plan_entry(self, plan_id: int, entry_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-plans#delete_plan_entry

        Deletes one or more existing test runs from a plan.
        :param plan_id: The ID of the test plan
        :param entry_id: The ID of the test plan entry (note: not the test run ID)
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_plan_entry/{plan_id}/{entry_id}')


class Priorities(BaseCategory):

    def get_priorities(self) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-priorities#get_priorities

        Returns a list of available priorities.
        :return: response
        """
        return self._session.request(METHODS.GET, 'get_priorities')


class Projects(BaseCategory):

    def get_project(self, project_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-projects#get_project

        Returns an existing project.

        :param project_id: The ID of the project
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_project/{project_id}')

    def get_projects(self, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-projects#get_projects

        Returns the list of available projects.

        :param kwargs: filter
            :key is_completed: int - 1 to return completed projects only. 0 to return active projects only.
        :return: response
        """
        return self._session.request(METHODS.GET, 'get_projects', params=kwargs)

    def add_project(self, name: str, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-projects#add_project

        Creates a new project (admin status required).

        :param name: The name of the project (required)
            :key announcement: str - The description of the project
            :key show_announcement: bool - True if the announcement should be displayed on the project's
                                            overview page and false otherwise
            :key suite_mode: int - 	The suite mode of the project (1 for single suite mode,
                                    2 for single suite + baselines, 3 for multiple suites) (added with TestRail 4.0)
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(METHODS.POST, 'add_project', json=data)

    def update_project(self, project_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-projects#update_project

        Updates an existing project (admin status required; partial updates are supported,
        i.e. you can submit and update specific fields only).

        :param project_id: The ID of the project
        :param kwargs: In addition to the POST fields supported by add_project, this method also supports
            :key is_completed: bool - Specifies whether a project is considered completed or not
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_project/{project_id}', json=kwargs)

    def delete_project(self, project_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-projects#delete_project

        Deletes an existing project (admin status required).

        :param project_id: The ID of the project
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_project/{project_id}')


class Results(BaseCategory):

    def get_results(self, test_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-results#get_results

        Returns a list of test results for a test.

        :param test_id: The ID of the test
        :param kwargs: filters
            :key limit/offset: int - Limit the result to :limit test results. Use :offset to skip records.
            :key status_id: int(list) - A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_results/{test_id}', params=kwargs)

    def get_results_for_case(self, run_id: int, case_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-results#get_results_for_case

        Returns a list of test results for a test run and case combination.

        The difference to get_results is that this method expects a test run + test case instead of a test.
        In TestRail, tests are part of a test run and the test cases are part of the related test suite.
        So, when you create a new test run, TestRail creates a test for each test case found in the test suite
        of the run. You can therefore think of a test as an “instance” of a test case which can have test results,
        comments and a test status. Please also see TestRail's getting started guide for more details about the
        differences between test cases and tests.

        :param run_id: The ID of the test run
        :param case_id: The ID of the test case
        :param kwargs: filters
            :key limit/offset: int - Limit the result to :limit test results. Use :offset to skip records.
            :key status_id: int(list) - A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_results_for_case/{run_id}/{case_id}', params=kwargs)

    def get_results_for_run(self, run_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-results#get_results_for_run

        Returns a list of test results for a test run.
        Requires TestRail 4.0 or later.

        :param run_id: The ID of the test run
        :param kwargs: filters
            :key created_after: int - Only return test results created after this date (as UNIX timestamp).
            :key created_before: int - Only return test results created before this date (as UNIX timestamp).
            :key created_by: int(list) - A comma-separated list of creators (user IDs) to filter by.
            :key limit/offset: int - Limit the result to :limit test results. Use :offset to skip records.
            :key status_id: int(list) - A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_results_for_run/{run_id}', params=kwargs)

    def add_result(self, test_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-results#add_result

        Adds a new test result, comment or assigns a test.
        It's recommended to use add_results instead if you plan to add results for multiple tests.

        :param test_id: The ID of the test the result should be added to
            :key status_id: int - The ID of the test status. The built-in system statuses have the following IDs:
                                    1 - Passed
                                    2 - Blocked
                                    3 - Untested (not allowed when adding a result)
                                    4 - Retest
                                    5 - Failed
                                    You can get a full list of system and custom statuses via get_statuses.
            :key comment: str - The comment / description for the test result
            :key version: str - The version or build you tested against
            :key elapsed: str - The time it took to execute the test, e.g. "30s" or "1m 45s"
            :key defects: str - A comma-separated list of defects to link to the test result
            :key assignedto_id: int - The ID of a user the test should be assigned to
        :return: response
        """
        return self._session.request(METHODS.POST, f'add_result/{test_id}', json=kwargs)

    def add_result_for_case(self, run_id: int, case_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-results#add_result_for_case

        Adds a new test result, comment or assigns a test (for a test run and case combination).
        It's recommended to use add_results_for_cases instead if you plan to add results for multiple test cases.

        The difference to add_result is that this method expects a test run + test case instead of a test.
        In TestRail, tests are part of a test run and the test cases are part of the related test suite.
        So, when you create a new test run, TestRail creates a test for each test case found in the test suite
        of the run. You can therefore think of a test as an “instance” of a test case which can have test results,
        comments and a test status. Please also see TestRail's getting started guide for more details about the
        differences between test cases and tests.

        :param run_id: The ID of the test run
        :param case_id: The ID of the test case
        :param kwargs: This method supports the same POST fields as add_result.
        :return: response
        """
        return self._session.request(METHODS.POST, f'add_result_for_case/{run_id}/{case_id}', json=kwargs)

    def add_results(self, run_id: int, results: List[dict]) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-results#add_results

        This method expects an array of test results (via the 'results' field, please see below).
        Each test result must specify the test ID and can pass in the same fields as add_result,
        namely all test related system and custom fields.

        Please note that all referenced tests must belong to the same test run.

        :param run_id: The ID of the test run the results should be added to
        :param results: List[dict]
            This method expects an array of test results (via the 'results' field, please see below).
            Each test result must specify the test ID and can pass in the same fields as add_result,
            namely all test related system and custom fields.

            Please note that all referenced tests must belong to the same test run.
        :return: response
        """
        return self._session.request(METHODS.POST, f'add_results/{run_id}', json={'results': results})

    def add_results_for_cases(self, run_id: int, results: List[dict]) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-results#add_results_for_cases

        Adds one or more new test results, comments or assigns one or more tests (using the case IDs).
        Ideal for test automation to bulk-add multiple test results in one step.

        Requires TestRail 3.1 or later

        :param run_id: The ID of the test run the results should be added to
        :param results: List[dict]
            This method expects an array of test results (via the 'results' field, please see below).
            Each test result must specify the test case ID and can pass in the same fields as add_result,
            namely all test related system and custom fields.

            The difference to add_results is that this method expects test case IDs instead of test IDs.
            Please see add_result_for_case for details.

            Please note that all referenced tests must belong to the same test run.
        :return: response
        """
        return self._session.request(METHODS.POST, f'add_results_for_cases/{run_id}', json={'results': results})


class ResultFields(BaseCategory):

    def get_result_fields(self) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-results-fields#get_result_fields

        Returns a list of available test result custom fields.

        :return: response
        """
        return self._session.request(METHODS.GET, 'get_result_fields')


class Runs(BaseCategory):

    def get_run(self, run_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-runs#get_run

        Returns an existing test run. Please see get_tests for the list of included tests in this run.

        :param run_id: The ID of the test run
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_run/{run_id}')

    def get_runs(self, project_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-runs#get_runs

        Returns a list of test runs for a project. Only returns those test runs that are not part of a test plan
        (please see get_plans/get_plan for this).

        :param project_id: The ID of the project
        :param kwargs: filters
            :key created_after: int - Only return test runs created after this date (as UNIX timestamp).
            :key created_before: int - Only return test runs created before this date (as UNIX timestamp).
            :key created_by: int(list) - A comma-separated list of creators (user IDs) to filter by.
            :key is_completed: int - 1 to return completed test runs only. 0 to return active test runs only.
            :key limit/offset: int - Limit the result to :limit test runs. Use :offset to skip records.
            :key milestone_id: int(list) - A comma-separated list of milestone IDs to filter by.
            :key suite_id: int(list) - A comma-separated list of test suite IDs to filter by.
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_runs/{project_id}', params=kwargs)

    def add_run(self, project_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-runs#add_run

        Creates a new test run.

        :param project_id: The ID of the project the test run should be added to
            :key suite_id: int - The ID of the test suite for the test run
                                (optional if the project is operating in single suite mode, required otherwise)
            :key name: str - The name of the test run
            :key description: str - The description of the test run
            :key milestone_id: int - The ID of the milestone to link to the test run
            :key assignedto_id: int - The ID of the user the test run should be assigned to
            :key include_all: bool - True for including all test cases of the test suite and false for a
                                        custom case selection (default: true)
            :key case_ids: list - An array of case IDs for the custom case selection
        :return: response
        """
        return self._session.request(METHODS.POST, f'add_run/{project_id}', json=kwargs)

    def update_run(self, run_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-runs#update_run

        Updates an existing test run (partial updates are supported,
        i.e. you can submit and update specific fields only).

        :param run_id: The ID of the test run
        :param kwargs: With the exception of the suite_id and assignedto_id fields,
                        this method supports the same POST fields as add_run.
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_run/{run_id}', json=kwargs)

    def close_run(self, run_id: int) -> Optional[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-runs#close_run

        Closes an existing test run and archives its tests & results.

        :param run_id: The ID of the test run
        :return: response
        """
        return self._session.request(METHODS.POST, f'close_run/{run_id}')

    def delete_run(self, run_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-runs#delete_run

        Deletes an existing test run.

        :param run_id: The ID of the test run
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_run/{run_id}')


class Sections(BaseCategory):

    def get_section(self, section_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-sections#get_section

        Returns an existing section.

        :param section_id: The ID of the section
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_section/{section_id}')

    def get_sections(self, project_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-sections#get_sections

        Returns a list of sections for a project and test suite.

        :param project_id: The ID of the project
        :param kwargs:
                :key suite_id: The ID of the test suite (optional if the project is operating in single suite mode)
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_sections/{project_id}', params=kwargs)

    def add_section(self, project_id: int, name: str, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-sections#add_section

        Creates a new section.

        :param project_id: The ID of the project
        :param name: The name of the section (required)
            :key description: str - The description of the section (added with TestRail 4.0)
            :key suite_id: int - The ID of the test suite (ignored if the project is operating in single suite mode,
                                                            required otherwise)
            :key parent_id: int - The ID of the parent section (to build section hierarchies)
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(METHODS.POST, f'add_section/{project_id}', json=data)

    def update_section(self, section_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-sections#update_section

        Updates an existing section (partial updates are supported,
        i.e. you can submit and update specific fields only).

        :param section_id: The ID of the section
            :key name: str - The name of the section
            :key description: str - The description of the section (added with TestRail 4.0)
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_section/{section_id}', json=kwargs)

    def delete_section(self, section_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-sections#delete_section

        Deletes an existing section.

        :param section_id: The ID of the section
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_section/{section_id}')


class Statuses(BaseCategory):

    def get_statuses(self) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-statuses#get_statuses

        Returns a list of available test statuses.

        :return: response
        """
        return self._session.request(METHODS.GET, 'get_statuses')


class Suites(BaseCategory):

    def get_suite(self, suite_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-suites#get_suite

        Returns an existing test suite.

        :param suite_id: The ID of the test suite
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_suite/{suite_id}')

    def get_suites(self, project_id: int) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-suites#get_suites

        Returns a list of test suites for a project.

        :param project_id: The ID of the project
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_suites/{project_id}')

    def add_suite(self, project_id: int, name: str, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-suites#add_suite

        Creates a new test suite.

        :param project_id: The ID of the project the test suite should be added to
        :param name: The name of the test suite (required)
            :key description: str - The description of the test suite
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(METHODS.POST, f'add_suite/{project_id}', json=data)

    def update_suite(self, suite_id: int, **kwargs) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-suites#update_suite

        Updates an existing test suite (partial updates are supported,
        i.e. you can submit and update specific fields only).
        :param suite_id: The ID of the test suite
        :param kwargs: This methods supports the same POST fields as add_suite.
        :return: response
        """
        return self._session.request(METHODS.POST, f'update_suite/{suite_id}', json=kwargs)

    def delete_suite(self, suite_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-suites#delete_suite

        Deletes an existing test suite.

        :param suite_id: The ID of the test suite
        :return: response
        """
        return self._session.request(METHODS.POST, f'delete_suite/{suite_id}')


class Template(BaseCategory):

    def get_templates(self, project_id: int) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-templates#get_templates

        Returns a list of available templates (requires TestRail 5.2 or later).

        :param project_id: The ID of the project
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_templates/{project_id}')


class Tests(BaseCategory):

    def get_test(self, test_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-tests#get_test

        Returns an existing test.
        If you interested in the test results rather than the tests, please see get_results instead.

        :param test_id: The ID of the test
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_test/{test_id}')

    def get_tests(self, run_id: int, **kwargs) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-tests#get_tests

        Returns a list of tests for a test run.

        :param run_id: The ID of the test run
        :param kwargs: filters
            :key status_id: int(list) - A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_tests/{run_id}', params=kwargs)


class Users(BaseCategory):

    def get_user(self, user_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-users#get_user

        Returns an existing user.

        :param user_id: The ID of the user
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_user/{user_id}')

    def get_user_by_email(self, email: str) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-users#get_user_by_email

        Returns an existing user by his/her email address.

        :param email: The email address to get the user for
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_user_by_email', params={'email': email})

    def get_users(self) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-users#get_users

        Returns a list of users.

        :return: response
        """
        return self._session.request(METHODS.GET, 'get_users')


class Attachments(BaseCategory):

    def add_attachment_to_result(self, result_id: int, path: Union[str, Path]) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-attachments#add_attachment_to_result

        Adds attachment to a result based on the result ID. The maximum allowable upload size is set to 256mb.

        :param result_id: The ID of the result the attachment should be added to
        :param path: The path to the file
        :return: response
        """
        return self._session.attachment_request(METHODS.POST, f'add_attachment_to_result/{result_id}', path)

    def add_attachment_to_result_for_case(self, result_id: int, case_id: int, path: Union[str, Path]):
        """
        http://docs.gurock.com/testrail-api2/reference-attachments#add_attachment_to_result_for_case

        Adds attachment to a result based on a combination of result and test case IDs.

        :param result_id: The ID of the result the attachment should be added to
        :param case_id: The ID of the test case
        :param path: The path to the file
        :return: response
        """
        warnings.warn('Method removed from official documentation', DeprecationWarning, stacklevel=2)
        # return self._session.attachment_request(
        #     METHODS.POST,
        #     f'add_attachment_to_result_for_case/{result_id}/{case_id}',
        #     path
        # )

    def get_attachments_for_case(self, case_id: int) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-attachments#get_attachments_for_case

        Returns a list of attachments for a test case.

        :param case_id: The ID of the test case
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_attachments_for_case/{case_id}')

    def get_attachments_for_test(self, test_id: int) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-attachments#get_attachments_for_test

        Returns a list of attachments for test results.

        :param test_id:
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_attachments_for_test/{test_id}')

    def get_attachment(self, attachment_id: int, path: Union[str, Path]) -> Path:
        """
        http://docs.gurock.com/testrail-api2/reference-attachments#get_attachment

        Returns the requested attachment identified by attachment_id.

        :param attachment_id:
        :param path: Path
        :return: Path
        """
        return self._session.get_attachment(METHODS.GET, f'get_attachment/{attachment_id}', path)

    def delete_attachment(self, attachment_id: int) -> None:
        """
        http://docs.gurock.com/testrail-api2/reference-attachments#delete_attachment

        Deletes the specified attachment identified by attachment_id.

        :param attachment_id:
        :return: None
        """
        return self._session.request(METHODS.POST, f'delete_attachment/{attachment_id}')


class Reports(BaseCategory):

    def get_reports(self, project_id: int) -> List[dict]:
        """
        http://docs.gurock.com/testrail-api2/reference-reports#get_reports

        Returns a list of API available reports by project.

        :param project_id: The ID of the project for which you want a list of API accessible reports
        :return: response
        """
        return self._session.request(METHODS.GET, f'get_reports/{project_id}')

    def run_report(self, report_template_id: int) -> dict:
        """
        http://docs.gurock.com/testrail-api2/reference-reports#run_report

        Executes the report identified using the :report_id parameter and returns URL's for
        accessing the report in HTML and PDF format.

        :param report_template_id:
        :return: response
        """
        return self._session.request(METHODS.GET, f'run_report/{report_template_id}')
