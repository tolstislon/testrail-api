"""
TestRail API categories
"""

from pathlib import Path
from typing import List, Optional, Union

from ._enums import METHODS


class _MetaCategory:
    """Meta Category"""

    def __init__(self, session) -> None:
        self._session = session


class Attachments(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/attachments"""

    def add_attachment_to_plan(self, plan_id: int, path: Union[str, Path]) -> dict:
        """
        Adds an attachment to a test plan. The maximum allowable upload size is
        set to 256mb.
        Requires TestRail 6.3 or later
        :param plan_id:
            The ID of the test plan the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self._session.attachment_request(
            METHODS.POST, "add_attachment_to_plan/{}".format(plan_id), path
        )

    def add_attachment_to_plan_entry(
        self, plan_id: int, entry_id: int, path: Union[str, Path]
    ) -> dict:
        """
        Adds an attachment to a test plan entry. The maximum allowable upload size is
        set to 256mb.
        Requires TestRail 6.3 or later
        :param plan_id:
            The ID of the test plan containing the entry
        :param entry_id:
            The ID of the test plan entry the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self._session.attachment_request(
            METHODS.POST,
            "add_attachment_to_plan_entry/{}/{}".format(plan_id, entry_id),
            path,
        )

    def add_attachment_to_result(self, result_id: int, path: Union[str, Path]) -> dict:
        """
        Adds attachment to a result based on the result ID.
        The maximum allowable upload size is set to 256mb.
        Requires TestRail 5.7 or later

        :param result_id:
            The ID of the result the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self._session.attachment_request(
            METHODS.POST, "add_attachment_to_result/{}".format(result_id), path
        )

    def add_attachment_to_run(self, run_id: int, path: Union[str, Path]) -> dict:
        """
        Adds attachment to test run.
        The maximum allowable upload size is set to 256mb.
        Requires TestRail 6.3 or later

        :param run_id:
            The ID of the test run the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self._session.attachment_request(
            METHODS.POST, "add_attachment_to_run/{}".format(run_id), path
        )

    def get_attachments_for_case(self, case_id: int) -> List[dict]:
        """
        Returns a list of attachments for a test case.
        Requires TestRail 5.7 or later

        :param case_id:
            The ID of the test case
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_attachments_for_case/{}".format(case_id)
        )

    def get_attachments_for_plan(self, plan_id: int) -> List[dict]:
        """
        Returns a list of attachments for a test plan.
        Requires TestRail 6.3 or later

        :param plan_id:
            The ID of the test plan to retrieve attachments from
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_attachments_for_plan/{}".format(plan_id)
        )

    def get_attachments_for_plan_entry(self, plan_id: int, entry_id: int) -> List[dict]:
        """
        Returns a list of attachments for a test plan entry.
        Requires TestRail 6.3 or later

        :param plan_id:
            The ID of the test plan containing the entry
        :param entry_id:
            The ID of the test plan entry to retrieve attachments from
        :return: response
        """
        return self._session.request(
            METHODS.GET,
            "get_attachments_for_plan_entry/{}/{}".format(plan_id, entry_id),
        )

    def get_attachments_for_run(self, run_id: int) -> List[dict]:
        """
        Returns a list of attachments for a test run.
        Requires TestRail 6.3 or later

        :param run_id:
            The ID of the test run to retrieve attachments from
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_attachments_for_run/{}".format(run_id)
        )

    def get_attachments_for_test(self, test_id: int) -> List[dict]:
        """
        Returns a list of attachments for test results.
        Requires TestRail 5.7 or later

        :param test_id:
            The ID of the test
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_attachments_for_test/{}".format(test_id)
        )

    def get_attachment(self, attachment_id: int, path: Union[str, Path]) -> Path:
        """
        Returns the requested attachment identified by attachment_id.
        Requires TestRail 5.7 or later

        :param attachment_id:
        :param path: Path
        :return: Path
        """
        return self._session.get_attachment(
            METHODS.GET, "get_attachment/{}".format(attachment_id), path
        )

    def delete_attachment(self, attachment_id: int) -> None:
        """
        Deletes the specified attachment identified by attachment_id.
        Requires TestRail 5.7 or later

        :param attachment_id:
        :return: None
        """
        return self._session.request(
            METHODS.POST, "delete_attachment/{}".format(attachment_id)
        )


class Cases(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/cases"""

    def get_case(self, case_id: int) -> dict:
        """
        Returns an existing test case.

        :param case_id:
            The ID of the test case
        :return: response
        """
        return self._session.request(METHODS.GET, "get_case/{}".format(case_id))

    def get_cases(self, project_id: int, **kwargs) -> List[dict]:
        """
        Returns a list of test cases for a test suite or specific section in a
        test suite.

        :param project_id:
            The ID of the project
        :param kwargs:
            :key suite_id: int
                The ID of the test suite (optional if the project is operating in
                single suite mode)
            :key created_after: int/datetime
                Only return test cases created after this date (as UNIX timestamp).
            :key created_before: int/datetime
                Only return test cases created before this date (as UNIX timestamp).
            :key created_by: List[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key filter: str
                Only return cases with matching filter string in the case title
            :key limit: int
                The number of test cases the response should return
            :key milestone_id: List[int] or comma-separated string
                A comma-separated list of milestone IDs to filter by (not available
                if the milestone field is disabled for the project).
            :key offset: int
                Where to start counting the tests cases from (the offset)
            :key priority_id: List[int] or comma-separated string
                A comma-separated list of priority IDs to filter by.
            :key section_id: int
                The ID of a test case section
            :key template_id: List[int] or comma-separated string
                A comma-separated list of template IDs to filter by
                (requires TestRail 5.2 or later)
            :key type_id: List[int] or comma-separated string
                A comma-separated list of case type IDs to filter by.
            :key updated_after: int/datetime
                Only return test cases updated after this date (as UNIX timestamp).
            :key updated_before: int/datetime
                Only return test cases updated before this date (as UNIX timestamp).
            :key updated_by: List[int] or comma-separated string
                A comma-separated list of user IDs who updated test cases to filter by.
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_cases/{}".format(project_id), params=kwargs
        )

    def add_case(self, section_id: int, title: str, **kwargs) -> dict:
        """
        Creates a new test case.

        :param section_id:
            The ID of the section the test case should be added to
        :param title:
            The title of the test case (required)
        :param kwargs:
            :key template_id: int
                The ID of the template (field layout) (requires TestRail 5.2 or later)
            :key type_id: int
                The ID of the case type
            :key priority_id: int
                The ID of the case priority
            :key estimate: str
                The estimate, e.g. "30s" or "1m 45s"
            :key milestone_id: int
                The ID of the milestone to link to the test case
            :key refs: str
                A comma-separated list of references/requirements

        Custom fields are supported as well and must be submitted with their
        system name, prefixed with 'custom_', e.g.:
        {
            ..
            "custom_preconds": "These are the preconditions for a test case"
            ..
        }
        The following custom field types are supported:
            Checkbox: bool
                True for checked and false otherwise
            Date: str
                A date in the same format as configured for TestRail and API user
                (e.g. "07/08/2013")
            Dropdown: int
                The ID of a dropdown value as configured in the field configuration
            Integer: int
                A valid integer
            Milestone: int
                The ID of a milestone for the custom field
            Multi-select: list
                An array of IDs as configured in the field configuration
            Steps: list
                An array of objects specifying the steps. Also see the example below.
            String: str
                A valid string with a maximum length of 250 characters
            Text: str
                A string without a maximum length
            URL: str
                A string with matches the syntax of a URL
            User: int
                The ID of a user for the custom field

        :return: response
        """
        data = dict(title=title, **kwargs)
        return self._session.request(
            METHODS.POST, "add_case/{}".format(section_id), json=data
        )

    def update_case(self, case_id: int, **kwargs) -> dict:
        """
        Updates an existing test case (partial updates are supported, i.e.
        you can submit and update specific fields only).

        :param case_id: T
            he ID of the test case
        :param kwargs:
            :key title: str
                The title of the test case
            :key template_id: int
                The ID of the template
            :key type_id: int
                The ID of the case type
            :key priority_id: int
                The ID of the case priority
            :key estimate: str
                The estimate, e.g. "30s" or "1m 45s"
            :key milestone_id: int
                The ID of the milestone to link to the test case
            :key refs: str
                A comma-separated list of references/requirements
        :return: response
        """
        return self._session.request(
            METHODS.POST, "update_case/{}".format(case_id), json=kwargs
        )

    def delete_case(self, case_id: int) -> None:
        """
        Deletes an existing test case.

        :param case_id:
            The ID of the test case
        :return: response
        """
        return self._session.request(METHODS.POST, "delete_case/{}".format(case_id))


class CaseFields(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/case-fields"""

    def get_case_fields(self) -> List[dict]:
        """
        Returns a list of available test case custom fields.

        A custom field can have different configurations and options per project which
        is indicated by the configs field. To check if a custom field is applicable to
        a specific project (and to find out the field options for this project),
        the context of the field configuration must either be global (is_global) or
        include the ID of the project in project_ids.

        Also, the following list shows the available custom field types (type_id field):
            1 - String
            2 - Integer
            3 - Text
            4 - URL
            5 - Checkbox
            6 - Dropdown
            7 - User
            8 - Date
            9 - Milestone
            10 - Steps
            12 - Multi-select
        :return: response
        """
        return self._session.request(METHODS.GET, "get_case_fields")

    def add_case_field(
        self, type: str, name: str, label: str, **kwargs  # noqa
    ) -> dict:
        """
        Creates a new test case custom field.

        :param type: str
            The type identifier for the new custom field (required).
            The following types are supported:
                    String, Integer, Text, URL, Checkbox, Dropdown, User, Date,
                    Milestone, Steps, Multiselect
            You can pass the number of the type as well as the word, e.g. "5",
            "string", "String", "Dropdown", "12".
            The numbers must be sent as a string e.g {type: "5"} not {type: 5},
            otherwise you will get a 400 (Bad Request) response.
        :param name: str
            The name for new the custom field (required)
        :param label: str
            The label for the new custom field (required)
        :param kwargs:
            :key description: str
                The description for the new custom field
            :key include_all: bool
                Set flag to true if you want the new custom field included for
                all templates. Otherwise (false) specify the ID's of templates to be
                included as the next parameter (template_ids)
            :key template_ids: list
                ID's of templates new custom field will apply to if include_all is
                set to false
            :key configs: dict
                An object wrapped in an array with two default keys,
                'context' and 'options'
        :return: response
        """
        data = dict(type=type, name=name, label=label, **kwargs)
        return self._session.request(METHODS.POST, "add_case_field", json=data)


class CaseTypes(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/case-types"""

    def get_case_types(self) -> List[dict]:
        """
        Returns a list of available case types.

        The response includes an array of test case types.
        Each case type has a unique ID and a name.
        The is_default field is true for the default case type and false otherwise.

        :return: response
        """
        return self._session.request(METHODS.GET, "get_case_types")


class Configurations(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/configurations"""

    def get_configs(self, project_id: int) -> List[dict]:
        """
        Returns a list of available configurations, grouped by configuration groups.

        :param project_id:
            The ID of the project
        :return: response
        """
        return self._session.request(METHODS.GET, "get_configs/{}".format(project_id))

    def add_config_group(self, project_id: int, name: str) -> dict:
        """
        Creates a new configuration group (requires TestRail 5.2 or later).

        :param project_id:
            The ID of the project the configuration group should be added to
        :param name:
            The name of the configuration group (required)
        :return: response
        """
        return self._session.request(
            METHODS.POST, "add_config_group/{}".format(project_id), json={"name": name}
        )

    def add_config(self, config_group_id: int, name: str) -> dict:
        """
        Creates a new configuration (requires TestRail 5.2 or later).

        :param config_group_id:
            The ID of the configuration group the configuration should be added to
        :param name:
            The name of the configuration (required)
        :return: response
        """
        return self._session.request(
            METHODS.POST, "add_config/{}".format(config_group_id), json={"name": name}
        )

    def update_config_group(self, config_group_id: int, name: str) -> dict:
        """
        Updates an existing configuration group (requires TestRail 5.2 or later).

        :param config_group_id:
            The ID of the configuration group
        :param name:
            The name of the configuration group
        :return: response
        """
        return self._session.request(
            METHODS.POST,
            "update_config_group/{}".format(config_group_id),
            json={"name": name},
        )

    def update_config(self, config_id: int, name: str) -> dict:
        """
        Updates an existing configuration (requires TestRail 5.2 or later).

        :param config_id:
            The ID of the configuration
        :param name:
            The name of the configuration
        :return: response
        """
        return self._session.request(
            METHODS.POST, "update_config/{}".format(config_id), json={"name": name}
        )

    def delete_config_group(self, config_group_id: int) -> None:
        """
        Deletes an existing configuration group and its configurations
        (requires TestRail 5.2 or later).

        :param config_group_id:
            The ID of the configuration group
        :return: response
        """
        return self._session.request(
            METHODS.POST, "delete_config_group/{}".format(config_group_id)
        )

    def delete_config(self, config_id: int) -> None:
        """
        Deletes an existing configuration (requires TestRail 5.2 or later).

        :param config_id:
            The ID of the configuration
        :return: response
        """
        return self._session.request(METHODS.POST, "delete_config/{}".format(config_id))


class Milestones(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/milestones"""

    def get_milestone(self, milestone_id: int) -> dict:
        """
        Returns an existing milestone.

        :param milestone_id:
            The ID of the milestone
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_milestone/{}".format(milestone_id)
        )

    def get_milestones(self, project_id: int, **kwargs) -> List[dict]:
        """
        Returns the list of milestones for a project.

        :param project_id:
            The ID of the project
        :param kwargs:
            :key is_completed: int/bool
                1/True to return completed milestones only.
                0/False to return open (active/upcoming) milestones only
                (available since TestRail 4.0).
            :key is_started: int/bool
                1/True to return started milestones only.
                0/False to return upcoming milestones only
                            (available since TestRail 5.3).
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_milestones/{}".format(project_id), params=kwargs
        )

    def add_milestone(self, project_id: int, name: str, **kwargs) -> dict:
        """
        Creates a new milestone.

        :param project_id:
            The ID of the project the milestone should be added to
        :param name: str
            The name of the milestone (required)
        :param kwargs:
            :key description: str
                The description of the milestone
            :key due_on: int/datetime
                The due date of the milestone (as UNIX timestamp)
            :key parent_id: int
                The ID of the parent milestone, if any (for sub-milestones)
                (available since TestRail 5.3)
            :key refs: str
                A comma-separated list of references/requirements
                (available since TestRail 6.4)
            :key start_on: int/datetime
                The scheduled start date of the milestone (as UNIX timestamp)
                (available since TestRail 5.3)
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(
            METHODS.POST, "add_milestone/{}".format(project_id), json=data
        )

    def update_milestone(self, milestone_id: int, **kwargs) -> dict:
        """
        Updates an existing milestone (partial updates are supported, i.e.
        you can submit and update specific fields only).

        :param milestone_id:
            The ID of the milestone
        :param kwargs:
            :key is_completed: bool
                True if a milestone is considered completed and false otherwise
            :key is_started: bool
                True if a milestone is considered started and false otherwise
            :key parent_id: int
                The ID of the parent milestone, if any (for sub-milestones)
                (available since TestRail 5.3)
            :key start_on: int/datetime
                The scheduled start date of the milestone (as UNIX timestamp)
                (available since TestRail 5.3)
        :return: response
        """
        return self._session.request(
            METHODS.POST, "update_milestone/{}".format(milestone_id), json=kwargs
        )

    def delete_milestone(self, milestone_id: int) -> None:
        """
        Deletes an existing milestone.

        :param milestone_id:
            The ID of the milestone
        :return: response
        """
        return self._session.request(
            METHODS.POST, "delete_milestone/{}".format(milestone_id)
        )


class Plans(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/plans"""

    def get_plan(self, plan_id: int) -> dict:
        """
        Returns an existing test plan.

        :param plan_id:
            The ID of the test plan
        :return: response
        """
        return self._session.request(METHODS.GET, "get_plan/{}".format(plan_id))

    def get_plans(self, project_id: int, **kwargs) -> List[dict]:
        """
        Returns a list of test plans for a project.

        This method will return up to 250 entries in the response array.
        To retrieve additional entries, you can make additional requests
        using the offset filter described in the Request filters section below.

        :param project_id:
            The ID of the project
        :param kwargs: filters
            :key created_after: int/datetime
                Only return test plans created after this date (as UNIX timestamp).
            :key created_before: int/datetime
                Only return test plans created before this date (as UNIX timestamp).
            :key created_by: List[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key is_completed: int/bool
                1/True to return completed test plans only.
                0/False to return active test plans only.
            :key limit/offset: int
                Limit the result to :limit test plans. Use :offset to skip records.
            :key milestone_id: List[int] or comma-separated string
                A comma-separated list of milestone IDs to filter by.
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_plans/{}".format(project_id), params=kwargs
        )

    def add_plan(self, project_id: int, name: str, **kwargs) -> dict:
        """
        Creates a new test plan.

        :param project_id:
            The ID of the project the test plan should be added to
        :param name:
            The name of the test plan (required)
        :param kwargs:
            :key description: str
                The description of the test plan
            :key milestone_id: int
                The ID of the milestone to link to the test plan
            :key entries: list
                An array of objects describing the test runs of the plan,
                see the example below and add_plan_entry
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(
            METHODS.POST, "add_plan/{}".format(project_id), json=data
        )

    def add_plan_entry(self, plan_id: int, suite_id: int, **kwargs) -> dict:
        """
        Adds one or more new test runs to a test plan.

        :param plan_id:
            The ID of the plan the test runs should be added to
        :param suite_id:
            The ID of the test suite for the test run(s) (required)
        :param kwargs:
            :key name: str
                The name of the test run(s)
            :key description: str
                The description of the test run(s) (requires TestRail 5.2 or later)
            :key assignedto_id: int
                The ID of the user the test run(s) should be assigned to
            :key include_all: bool
                True for including all test cases of the test suite and false for a
                custom case selection (default: true)
            :key case_ids: list
                An array of case IDs for the custom case selection
            :key config_ids: list
                An array of configuration IDs used for the test runs of the test
                plan entry
            :key refs: str
                A string of external requirement IDs, separated by commas.
                (requires TestRail 6.3 or later)
            :key runs: list
                An array of test runs with configurations,
                please see the example below for details
        :return: response
        """
        data = dict(suite_id=suite_id, **kwargs)
        return self._session.request(
            METHODS.POST, "add_plan_entry/{}".format(plan_id), json=data
        )

    def add_run_to_plan_entry(
        self, plan_id: int, entry_id: int, config_ids: List[int], **kwargs
    ):
        """
        Adds a new test run to a test plan entry (using configurations).
        Requires TestRail 6.4 or later

        :param plan_id:
            The ID of the plan the test runs should be added to
        :param entry_id:
            The ID of the test plan entry
        :param config_ids:
            An array of configuration IDs used for the test run of the
            test plan entry (Required)
        :param kwargs:
            :key description: str
                The description of the test run
            :key assignedto_id: int
                The ID of the user the test run should be assigned to
            :key include_all: bool
                True for including all test cases of the test suite and false for
                a custom case selection
            :key case_ids: List[int]
                An array of case IDs for the custom case selection
                (Required if include_all is false)
            :key refs: str
                A comma-separated list of references/requirements
        :return: response
        """
        return self._session.request(
            METHODS.POST,
            "add_run_to_plan_entry/{}/{}".format(plan_id, entry_id),
            json=dict(config_ids=config_ids, **kwargs),
        )

    def update_plan(self, plan_id: int, **kwargs) -> dict:
        """
        Updates an existing test plan (partial updates are supported,
        i.e. you can submit and update specific fields only).

        :param plan_id:
            The ID of the test plan
        :param kwargs:
            With the exception of the entries field, this method supports the same
            POST fields as add_plan.
        :return: response
        """
        return self._session.request(
            METHODS.POST, "update_plan/{}".format(plan_id), json=kwargs
        )

    def update_plan_entry(self, plan_id: int, entry_id: int, **kwargs) -> dict:
        """
        Updates one or more existing test runs in a plan (partial updates are supported,
        i.e. you can submit and update specific fields only).

        :param plan_id:
            The ID of the test plan
        :param entry_id:
            The ID of the test plan entry (note: not the test run ID)
        :param kwargs:
            :key name: str
                The name of the test run(s)
            :key description: str
                The description of the test run(s) (requires TestRail 5.2 or later)
            :key assignedto_id: int
                The ID of the user the test run(s) should be assigned to
            :key include_all: bool
                True for including all test cases of the test suite and false for a
                custom case selection (default: true)
            :key case_ids: list
                An array of case IDs for the custom case selection
            :key refs: str
                A string of external requirement IDs, separated by commas.
                (requires TestRail 6.3 or later)
        :return: response
        """
        return self._session.request(
            METHODS.POST,
            "update_plan_entry/{}/{}".format(plan_id, entry_id),
            json=kwargs,
        )

    def update_run_in_plan_entry(self, plan_id: int, run_id: int, **kwargs):
        """
        Updates a run inside a plan entry which uses configurations
        Requires TestRail 6.4 or later

        :param plan_id:
            The ID of the test plan
        :param run_id:
            The ID of the test run
        :param kwargs:
            :key description: str
                The description of the test run
            :key assignedto_id: int
                The ID of the user the test run should be assigned to
            :key include_all: bool
                True for including all test cases of the test suite and false for
                a custom case selection
            :key case_ids: List[int]
                An array of case IDs for the custom case selection.
                (Required if include_all is false)
            :key refs: str
                A comma-separated list of references/requirements
        :return: response
        """
        return self._session.request(
            METHODS.POST,
            "update_run_in_plan_entry/{}/{}".format(plan_id, run_id),
            json=kwargs,
        )

    def close_plan(self, plan_id: int) -> dict:
        """
        Closes an existing test plan and archives its test runs & results.

        :param plan_id:
            The ID of the test plan
        :return: response
        """
        return self._session.request(METHODS.POST, "close_plan/{}".format(plan_id))

    def delete_plan(self, plan_id: int) -> None:
        """
        Deletes an existing test plan.

        :param plan_id:
            The ID of the test plan
        :return: response
        """
        return self._session.request(METHODS.POST, "delete_plan/{}".format(plan_id))

    def delete_plan_entry(self, plan_id: int, entry_id: int) -> None:
        """
        Deletes one or more existing test runs from a plan.

        :param plan_id:
            The ID of the test plan
        :param entry_id:
            The ID of the test plan entry (note: not the test run ID)
        :return: response
        """
        return self._session.request(
            METHODS.POST, "delete_plan_entry/{}/{}".format(plan_id, entry_id)
        )

    def delete_run_from_plan_entry(self, run_id: int):
        """
        Deletes a test run from a test plan entry

        :param run_id:
            The ID of the test run
        :return: response
        """
        return self._session.request(
            METHODS.POST, "delete_run_from_plan_entry/{}".format(run_id)
        )


class Priorities(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/priorities"""

    def get_priorities(self) -> List[dict]:
        """
        Returns a list of available priorities.

        :return: response
        """
        return self._session.request(METHODS.GET, "get_priorities")


class Projects(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/projects"""

    def get_project(self, project_id: int) -> dict:
        """
        Returns an existing project.

        :param project_id:
            The ID of the project
        :return: response
        """
        return self._session.request(METHODS.GET, "get_project/{}".format(project_id))

    def get_projects(self, **kwargs) -> List[dict]:
        """
        Returns the list of available projects.

        :param kwargs: filter
            :key is_completed: int/bool
                1/True to return completed projects only.
                0/False to return active projects only.
        :return: response
        """
        return self._session.request(METHODS.GET, "get_projects", params=kwargs)

    def add_project(self, name: str, **kwargs) -> dict:
        """
        Creates a new project (admin status required).

        :param name:
            The name of the project (required)
        :param kwargs:
            :key announcement: str
                The description of the project
            :key show_announcement: bool
                True if the announcement should be displayed on the project's overview
                page and false otherwise
            :key suite_mode: int
                The suite mode of the project
                    1 for single suite mode,
                    2 for single suite + baselines,
                    3 for multiple suite
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(METHODS.POST, "add_project", json=data)

    def update_project(self, project_id: int, **kwargs) -> dict:
        """
        Updates an existing project (admin status required; partial updates are
        supported, i.e. you can submit and update specific fields only).

        :param project_id:
            The ID of the project
        :param kwargs:
            :key name: str
                The name of the project
            :key announcement: str
                The description of the project
            :key show_annoucement: bool
                True if the annoucnement should be displayed on the project’s
                overview page and false otherwise
            :key is_completed: bool
                Specifies whether a project is considered completed or not
        :return: response
        """
        return self._session.request(
            METHODS.POST, "update_project/{}".format(project_id), json=kwargs
        )

    def delete_project(self, project_id: int) -> None:
        """
        Deletes an existing project (admin status required).

        :param project_id:
            The ID of the project
        :return: response
        """
        return self._session.request(
            METHODS.POST, "delete_project/{}".format(project_id)
        )


class Reports(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/reports"""

    def get_reports(self, project_id: int) -> List[dict]:
        """
        Returns a list of API available reports by project.

        :param project_id:
            The ID of the project for which you want a list of API accessible reports
        :return: response
        """
        return self._session.request(METHODS.GET, "get_reports/{}".format(project_id))

    def run_report(self, report_template_id: int) -> dict:
        """
        Executes the report identified using the :report_id parameter and returns
        URL's for accessing the report in HTML and PDF format.

        Requires TestRail 5.7 or later.

        :param report_template_id:
        :return: response
        """
        return self._session.request(
            METHODS.GET, "run_report/{}".format(report_template_id)
        )


class Results(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/results"""

    def get_results(self, test_id: int, **kwargs) -> List[dict]:
        """
        Returns a list of test results for a test.

        :param test_id:
            The ID of the test
        :param kwargs: filters
            :key limit/offset: int -
                Limit the result to :limit test results. Use :offset to skip records.
            :key status_id: List[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_results/{}".format(test_id), params=kwargs
        )

    def get_results_for_case(self, run_id: int, case_id: int, **kwargs) -> List[dict]:
        """
        Returns a list of test results for a test run and case combination.

        The difference to get_results is that this method expects a test run +
        test case instead of a test. In TestRail, tests are part of a test run and
        the test cases are part of the related test suite. So, when you create a new
        test run, TestRail creates a test for each test case found in the test suite
        of the run. You can therefore think of a test as an “instance” of a test case
        which can have test results, comments and a test status.
        Please also see TestRail's getting started guide for more details about the
        differences between test cases and tests.

        :param run_id:
            The ID of the test run
        :param case_id:
            The ID of the test case
        :param kwargs: filters
            :key limit/offset: int
                Limit the result to :limit test results. Use :offset to skip records.
            :key status_id: List[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self._session.request(
            METHODS.GET,
            "get_results_for_case/{}/{}".format(run_id, case_id),
            params=kwargs,
        )

    def get_results_for_run(self, run_id: int, **kwargs) -> List[dict]:
        """
        Returns a list of test results for a test run.

        This method uses the same response format as get_results.

        This method will return up to 250 entries in the response array.
        To retrieve additional entries, you can make additional requests using
        the offset filter described in the Request filters section below.

        :param run_id:
            The ID of the test run
        :param kwargs: filters
            :key created_after: int/datetime
                Only return test results created after this date (as UNIX timestamp).
            :key created_before: int/datetime
                Only return test results created before this date (as UNIX timestamp).
            :key created_by: List[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key limit/offset: int
                Limit the result to :limit test results. Use :offset to skip records.
            :key status_id: List[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_results_for_run/{}".format(run_id), params=kwargs
        )

    def add_result(self, test_id: int, **kwargs) -> List[dict]:
        """
        Adds a new test result, comment or assigns a test.
        It's recommended to use add_results instead if you plan to add results for
        multiple tests.

        :param test_id:
            The ID of the test the result should be added to
        :param kwargs:
            :key status_id: int
                The ID of the test status. The built-in system
                statuses have the following IDs:
                    1 - Passed
                    2 - Blocked
                    3 - Untested (not allowed when adding a result)
                    4 - Retest
                    5 - Failed
                You can get a full list of system and custom statuses via get_statuses.
            :key comment: str
                The comment / description for the test result
            :key version: str
                The version or build you tested against
            :key elapsed: str
                The time it took to execute the test, e.g. "30s" or "1m 45s"
            :key defects: str
                A comma-separated list of defects to link to the test result
            :key assignedto_id: int
                The ID of a user the test should be assigned to
        :return: response
        """
        return self._session.request(
            METHODS.POST, "add_result/{}".format(test_id), json=kwargs
        )

    def add_result_for_case(self, run_id: int, case_id: int, **kwargs) -> dict:
        """
        Adds a new test result, comment or assigns a test (for a test run and case
        combination). It's recommended to use add_results_for_cases instead if you
        plan to add results for multiple test cases.

        The difference to add_result is that this method expects a test run +
        test case instead of a test. In TestRail, tests are part of a test run and
        the test cases are part of the related test suite.
        So, when you create a new test run, TestRail creates a test for each test case
        found in the test suite of the run.
        You can therefore think of a test as an “instance” of a test case which can
        have test results, comments and a test status.
        Please also see TestRail's getting started guide for more details about the
        differences between test cases and tests.

        :param run_id:
            The ID of the test run
        :param case_id:
            The ID of the test case
        :param kwargs:
            This method supports the same POST fields as add_result.
        :return: response
        """
        return self._session.request(
            METHODS.POST,
            "add_result_for_case/{}/{}".format(run_id, case_id),
            json=kwargs,
        )

    def add_results(self, run_id: int, results: List[dict]) -> List[dict]:
        """
        This method expects an array of test results (via the 'results' field,
        please see below). Each test result must specify the test ID and can pass in
        the same fields as add_result, namely all test related system and custom fields.

        Please note that all referenced tests must belong to the same test run.

        :param run_id:
            The ID of the test run the results should be added to
        :param results: List[dict]
            This method expects an array of test results (via the 'results' field,
            please see below).
            Each test result must specify the test ID and can pass in the same fields
            as add_result, namely all test related system and custom fields.

            Please note that all referenced tests must belong to the same test run.
        :return: response
        """
        return self._session.request(
            METHODS.POST, "add_results/{}".format(run_id), json={"results": results}
        )

    def add_results_for_cases(self, run_id: int, results: List[dict]) -> List[dict]:
        """
        Adds one or more new test results, comments or assigns one or more tests
        (using the case IDs).
        Ideal for test automation to bulk-add multiple test results in one step.

        Requires TestRail 3.1 or later

        :param run_id:
            The ID of the test run the results should be added to
        :param results: List[dict]
            This method expects an array of test results (via the 'results' field,
            please see below). Each test result must specify the test case ID and
            can pass in the same fields as add_result, namely all test related
            system and custom fields.

            The difference to add_results is that this method expects test case IDs
            instead of test IDs. Please see add_result_for_case for details.

            Please note that all referenced tests must belong to the same test run.
        :return: response
        """
        return self._session.request(
            METHODS.POST,
            "add_results_for_cases/{}".format(run_id),
            json={"results": results},
        )


class ResultFields(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/result-fields"""

    def get_result_fields(self) -> List[dict]:
        """
        Returns a list of available test result custom fields.

        :return: response
        """
        return self._session.request(METHODS.GET, "get_result_fields")


class Runs(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/runs"""

    def get_run(self, run_id: int) -> dict:
        """
        Returns an existing test run. Please see get_tests for the list of included
        tests in this run.

        :param run_id:
            The ID of the test run
        :return: response
        """
        return self._session.request(METHODS.GET, "get_run/{}".format(run_id))

    def get_runs(self, project_id: int, **kwargs) -> List[dict]:
        """
        Returns a list of test runs for a project. Only returns those test runs that
        are not part of a test plan (please see get_plans/get_plan for this).

        :param project_id: The ID of the project
        :param kwargs: filters
            :key created_after: int/datetime
                Only return test runs created after this date (as UNIX timestamp).
            :key created_before: int/datetime
                Only return test runs created before this date (as UNIX timestamp).
            :key created_by: List[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key is_completed: int/bool
                1/True to return completed test runs only.
                0/False to return active test runs only.
            :key limit/offset: int
                Limit the result to :limit test runs. Use :offset to skip records.
            :key milestone_id: List[int] or comma-separated string
                A comma-separated list of milestone IDs to filter by.
            :key suite_id: List[int] or comma-separated string
                A comma-separated list of test suite IDs to filter by.
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_runs/{}".format(project_id), params=kwargs
        )

    def add_run(self, project_id: int, **kwargs) -> dict:
        """
        Creates a new test run.

        :param project_id:
            The ID of the project the test run should be added to
        :param kwargs:
            :key suite_id: int
                The ID of the test suite for the test run (optional if the project is
                operating in single suite mode, required otherwise)
            :key name: str
                The name of the test run
            :key description: str
                The description of the test run
            :key milestone_id: int
                The ID of the milestone to link to the test run
            :key assignedto_id: int
                The ID of the user the test run should be assigned to
            :key include_all: bool
                True for including all test cases of the test suite and false for a
                custom case selection (default: true)
            :key case_ids: list
                An array of case IDs for the custom case selection
            :key refs: str
                A comma-separated list of references/requirements
                (Requires TestRail 6.1 or later)
        :return: response
        """
        return self._session.request(
            METHODS.POST, "add_run/{}".format(project_id), json=kwargs
        )

    def update_run(self, run_id: int, **kwargs) -> dict:
        """
        Updates an existing test run (partial updates are supported,
        i.e. you can submit and update specific fields only).

        :param run_id:
            The ID of the test run
        :param kwargs:
            With the exception of the suite_id and assignedto_id fields,
            this method supports the same POST fields as add_run.
        :return: response
        """
        return self._session.request(
            METHODS.POST, "update_run/{}".format(run_id), json=kwargs
        )

    def close_run(self, run_id: int) -> Optional[dict]:
        """
        Closes an existing test run and archives its tests & results.

        :param run_id:
            The ID of the test run
        :return: response
        """
        return self._session.request(METHODS.POST, "close_run/{}".format(run_id))

    def delete_run(self, run_id: int) -> None:
        """
        Deletes an existing test run.

        :param run_id:
            The ID of the test run
        :return: response
        """
        return self._session.request(METHODS.POST, "delete_run/{}".format(run_id))


class Sections(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/sections"""

    def get_section(self, section_id: int) -> dict:
        """
        Returns an existing section.

        :param section_id:
            The ID of the section
        :return: response
        """
        return self._session.request(METHODS.GET, "get_section/{}".format(section_id))

    def get_sections(self, project_id: int, **kwargs) -> List[dict]:
        """
        Returns a list of sections for a project and test suite.

        :param project_id:
            The ID of the project
        :param kwargs:
            :key suite_id:
                The ID of the test suite (optional if the project is operating in
                single suite mode)
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_sections/{}".format(project_id), params=kwargs
        )

    def add_section(self, project_id: int, name: str, **kwargs) -> dict:
        """
        Creates a new section.

        :param project_id:
            The ID of the project
        :param name:
            The name of the section (required)
        :param kwargs:
            :key description: str
                The description of the section
            :key suite_id: int
                The ID of the test suite (ignored if the project is
                operating in single suite mode, required otherwise)
            :key parent_id: int
                The ID of the parent section (to build section hierarchies)
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(
            METHODS.POST, "add_section/{}".format(project_id), json=data
        )

    def update_section(self, section_id: int, **kwargs) -> dict:
        """
        Updates an existing section (partial updates are supported,
        i.e. you can submit and update specific fields only).

        :param section_id:
            The ID of the section
        :param kwargs:
            :key name: str
                The name of the section
            :key description: str
                The description of the section
        :return: response
        """
        return self._session.request(
            METHODS.POST, "update_section/{}".format(section_id), json=kwargs
        )

    def delete_section(self, section_id: int) -> None:
        """
        Deletes an existing section.

        :param section_id:
            The ID of the section
        :return: response
        """
        return self._session.request(
            METHODS.POST, "delete_section/{}".format(section_id)
        )


class Statuses(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/statuses"""

    def get_statuses(self) -> List[dict]:
        """
        Returns a list of available test statuses.

        :return: response
        """
        return self._session.request(METHODS.GET, "get_statuses")


class Suites(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/suites"""

    def get_suite(self, suite_id: int) -> dict:
        """
        Returns an existing test suite.

        :param suite_id:
            The ID of the test suite
        :return: response
        """
        return self._session.request(METHODS.GET, "get_suite/{}".format(suite_id))

    def get_suites(self, project_id: int) -> List[dict]:
        """
        Returns a list of test suites for a project.

        :param project_id:
            The ID of the project
        :return: response
        """
        return self._session.request(METHODS.GET, "get_suites/{}".format(project_id))

    def add_suite(self, project_id: int, name: str, **kwargs) -> dict:
        """
        Creates a new test suite.

        :param project_id:
            The ID of the project the test suite should be added to
        :param name:
            The name of the test suite (required)
        :param kwargs:
            :key description: str
                The description of the test suite
        :return: response
        """
        data = dict(name=name, **kwargs)
        return self._session.request(
            METHODS.POST, "add_suite/{}".format(project_id), json=data
        )

    def update_suite(self, suite_id: int, **kwargs) -> dict:
        """
        Updates an existing test suite (partial updates are supported,
        i.e. you can submit and update specific fields only).

        :param suite_id:
            The ID of the test suite
        :param kwargs:
            This methods supports the same POST fields as add_suite.
        :return: response
        """
        return self._session.request(
            METHODS.POST, "update_suite/{}".format(suite_id), json=kwargs
        )

    def delete_suite(self, suite_id: int) -> None:
        """
        Deletes an existing test suite.

        :param suite_id:
            The ID of the test suite
        :return: response
        """
        return self._session.request(METHODS.POST, "delete_suite/{}".format(suite_id))


class Template(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/templates"""

    def get_templates(self, project_id: int) -> List[dict]:
        """
        Returns a list of available templates (requires TestRail 5.2 or later).

        :param project_id:
            The ID of the project
        :return: response
        """
        return self._session.request(METHODS.GET, "get_templates/{}".format(project_id))


class Tests(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/tests"""

    def get_test(self, test_id: int) -> dict:
        """
        Returns an existing test.
        If you interested in the test results rather than the tests, please see
        get_results instead.

        :param test_id:
            The ID of the test
        :return: response
        """
        return self._session.request(METHODS.GET, "get_test/{}".format(test_id))

    def get_tests(self, run_id: int, **kwargs) -> List[dict]:
        """
        Returns a list of tests for a test run.

        :param run_id:
            The ID of the test run
        :param kwargs: filters
            :key status_id: List[str] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_tests/{}".format(run_id), params=kwargs
        )


class Users(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/users"""

    def get_user(self, user_id: int) -> dict:
        """
        Returns an existing user.

        :param user_id:
            The ID of the user
        :return: response
        """
        return self._session.request(METHODS.GET, "get_user/{}".format(user_id))

    def get_user_by_email(self, email: str) -> dict:
        """
        Returns an existing user by his/her email address.

        :param email:
            The email address to get the user for
        :return: response
        """
        return self._session.request(
            METHODS.GET, "get_user_by_email", params={"email": email}
        )

    def get_users(self, **kwargs) -> List[dict]:
        """
        Returns a list of users.
        :param kwargs:
            :key project_id: int
                The ID of the project for which you would like to retrieve
                user information. (Required for non-administrators.
                Requires TestRail 6.4 or later.)
        :return: response
        """
        return self._session.request(METHODS.GET, "get_users", params=kwargs)
