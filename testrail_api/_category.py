"""TestRail API categories."""

import itertools
from pathlib import Path
from typing import Any, Callable, Optional, Union

from ._enums import METHODS
from ._session import Session

OFFSET_MAX = 250
LIMIT_MAX = 250


def _bulk_api_method(func: Callable, resp_key: str, *args, **kwargs) -> list:
    """
    Get the objects handling the pagination via offset.

    If the size returned from the API is less than the offset value.
    """
    _response_objects = []
    for offset in itertools.count(0, OFFSET_MAX):
        kwargs.update({"offset": offset, "limit": LIMIT_MAX})
        _resp = func(*args, **kwargs)
        _response_objects.extend(_resp.get(resp_key))
        if _resp.get("size") < LIMIT_MAX:
            break
    return _response_objects


class _MetaCategory:
    """Meta Category."""

    @property
    def s(self) -> Session:
        return self._session

    def __call__(self, session: Session):  # noqa: ANN204 (3.9 and 3.10 no Self)
        self._session = session
        return self

    @staticmethod
    def _opt(params: dict[Any, Any]) -> dict[Any, Any]:
        return {k: v for k, v in params.items() if v is not None}

    def __get__(self, instance: Session, owner: type[Session]):  # noqa: ANN204 (3.9 and 3.10 no Self)
        return self(instance)


class Attachments(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/attachments."""

    def add_attachment_to_plan(self, plan_id: int, path: Union[str, Path]) -> dict:
        """
        Adds an attachment to a test plan.

        The maximum allowable upload size is set to 256 mb.
        Requires TestRail 6.3 or later.

        :param plan_id:
            The ID of the test plan the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self.s.attachment_request(METHODS.POST, f"add_attachment_to_plan/{plan_id}", path)

    def add_attachment_to_plan_entry(self, plan_id: int, entry_id: int, path: Union[str, Path]) -> dict:
        """
        Adds an attachment to a test plan entry.

        The maximum allowable upload size is set to 256 mb.
        Requires TestRail 6.3 or later.

        :param plan_id:
            The ID of the test plan containing the entry
        :param entry_id:
            The ID of the test plan entry the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self.s.attachment_request(
            METHODS.POST,
            f"add_attachment_to_plan_entry/{plan_id}/{entry_id}",
            path,
        )

    def add_attachment_to_result(self, result_id: int, path: Union[str, Path]) -> dict:
        """
        Adds attachment to a result based on the result ID.

        The maximum allowable upload size is set to 256 mb.
        Requires TestRail 5.7 or later.

        :param result_id:
            The ID of the result the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self.s.attachment_request(METHODS.POST, f"add_attachment_to_result/{result_id}", path)

    def add_attachment_to_run(self, run_id: int, path: Union[str, Path]) -> dict:
        """
        Adds attachment to test run.

        The maximum allowable upload size is set to 256 mb.
        Requires TestRail 6.3 or later.

        :param run_id:
            The ID of the test run the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self.s.attachment_request(METHODS.POST, f"add_attachment_to_run/{run_id}", path)

    def add_attachment_to_case(self, case_id: int, path: Union[str, Path]) -> dict:
        """
        Adds attachment to a case based on the case ID.

        The maximum allowable upload size is set to 256 mb.
        Requires TestRail 6.5.2 or later.

        :param case_id:
            The ID of the case the attachment should be added to
        :param path:
            The path to the file
        :return: dict
                ex: {"attachment_id": 443}
        """
        return self.s.attachment_request(METHODS.POST, f"add_attachment_to_case/{case_id}", path)

    def get_attachments_for_case(self, case_id: int, limit: int = 250, offset: int = 0) -> dict:
        """
        Returns a list of attachments for a test case.

        Requires TestRail 5.7 or later

        :param case_id: int
            The ID of the test case
        :param limit: int
            The number of attachments the response should return
            (The response size is 250 by default) (requires TestRail 6.7 or later)
        :param offset: int
            Where to start counting the attachments from (the offset)
            (requires TestRail 6.7 or later)
        :return: response
        """
        return self.s.get(
            endpoint=f"get_attachments_for_case/{case_id}",
            params={"limit": limit, "offset": offset},
        )

    def get_attachments_for_plan(self, plan_id: int, limit: int = 250, offset: int = 0) -> list[dict]:
        """
        Returns a list of attachments for a test plan.

        Requires TestRail 6.3 or later.

        :param plan_id:
            The ID of the test plan to retrieve attachments from
        :param limit:
            The number of attachments the response should return
            (The response size is 250 by default) (requires TestRail 6.7 or later)
        :param offset:
            Where to start counting the attachments from (the offset)
            (requires TestRail 6.7 or later)
        :return: response
        """
        return self.s.get(
            endpoint=f"get_attachments_for_plan/{plan_id}",
            params={"limit": limit, "offset": offset},
        )

    def get_attachments_for_plan_entry(self, plan_id: int, entry_id: int, **kwargs) -> list[dict]:
        """
        Returns a list of attachments for a test plan entry.

        Requires TestRail 6.3 or later.

        :param plan_id:
            The ID of the test plan containing the entry
        :param entry_id:
            The ID of the test plan entry to retrieve attachments from
        :param kwargs:
            :key limit/offset: int
                The number of attachments the response should return
        :return: response
        """
        return self.s.get(
            endpoint=f"get_attachments_for_plan_entry/{plan_id}/{entry_id}",
            params=kwargs,
        )

    def get_attachments_for_run(self, run_id: int, limit: int = 250, offset: int = 0) -> list[dict]:
        """
        Returns a list of attachments for a test run.

        Requires TestRail 6.3 or later.

        :param run_id:
            The ID of the test run to retrieve attachments from
        :param limit:
            The number of attachments the response should return
            (The response size is 250 by default) (requires TestRail 6.7 or later)
        :param offset:
            Where to start counting the attachments from (the offset)
            (requires TestRail 6.7 or later)
        :return: response
        """
        return self.s.get(
            endpoint=f"get_attachments_for_run/{run_id}",
            params={"limit": limit, "offset": offset},
        )

    def get_attachments_for_test(self, test_id: int, **kwargs) -> list[dict]:
        """
        Returns a list of attachments for test results.

        Requires TestRail 5.7 or later.

        :param test_id:
            The ID of the test
        :param kwargs:
            :key limit/offset: int
                The number of attachments the response should return
        :return: response
        """
        return self.s.get(endpoint=f"get_attachments_for_test/{test_id}", params=kwargs)

    def get_attachment(self, attachment_id: int, path: Union[str, Path]) -> Path:
        """
        Returns the requested attachment identified by attachment_id.

        Requires TestRail 5.7 or later.

        :param attachment_id:
            The ID of the test to retrieve attachments from
        :param path: Path
        :return: Path
        """
        return self._session.get_attachment(METHODS.GET, f"get_attachment/{attachment_id}", path)

    def delete_attachment(self, attachment_id: int) -> None:
        """
        Deletes the specified attachment identified by attachment_id.

        Requires TestRail 5.7 or later.

        :param attachment_id:
            The ID of the attachment to to delete
        :return: None
        """
        return self.s.post(endpoint=f"delete_attachment/{attachment_id}")

    def get_attachments_for_case_bulk(self, case_id: int) -> list[dict]:
        """
        Return the list of attachments from the case handling pagination.

        Requires TestRail 5.7 or later

        :param case_id:
            The ID of the test case to retrieve attachments from
        :return: List of attachments
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_attachments_for_case, "attachments", case_id)

    def get_attachments_for_plan_bulk(self, plan_id: int) -> list[dict]:
        """
        Return the list of attachments from the plan handling pagination.

        Requires TestRail 6.3 or later

        :param plan_id:
            The ID of the test plan to retrieve attachments from
        :return: List of attachments
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_attachments_for_plan, "attachments", plan_id)

    def get_attachments_for_run_bulk(self, run_id: int) -> list[dict]:
        """
        Return the list of attachments from the run handling pagination.

        Requires TestRail 6.3 or later

        :param run_id:
            The ID of the test run to retrieve attachments from
        :return: List of attachments
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_attachments_for_run, "attachments", run_id)

    def get_attachments_for_plan_entry_bulk(self, plan_id: int, entry_id: int) -> list[dict]:
        """
        Returns the list of attachments for the plan entry handling pagination.

        Requires TestRail 6.3 or later

        :param plan_id:
            The ID of the test plan containing the entry
        :param entry_id:
            The ID of the test plan entry to retrieve attachments from
        :return: List of attachments
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_attachments_for_plan_entry, "attachments", plan_id, entry_id)

    def get_attachments_for_test_bulk(self, test_id: int) -> list[dict]:
        """
        Return the list of attachments from the test handling pagination.

        Requires TestRail 6.3 or later

        :param test_id:
            The ID of the test to retrieve attachments from
        :return: List of attachments
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_attachments_for_test, "attachments", test_id)


class Cases(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/cases."""

    def get_case(self, case_id: int) -> dict:
        """
        Returns an existing test case.

        :param case_id:
            The ID of the test case
        :return: response
        """
        return self.s.get(endpoint=f"get_case/{case_id}")

    def get_cases(self, project_id: int, **kwargs) -> dict:
        """
        Returns a list of test cases for a project or specific test suite (if the project has multiple suites enabled).

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
            :key created_by: list[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key filter: str
                Only return cases with matching filter string in the case title
            :key limit: int
                The number of test cases the response should return
                (The response size is 250 by default) (requires TestRail 6.7 or later)
            :key milestone_id: list[int] or comma-separated string
                A comma-separated list of milestone IDs to filter by (not available
                if the milestone field is disabled for the project).
            :key offset: int
                Where to start counting the tests cases from (the offset)
                (requires TestRail 6.7 or later)
            :key priority_id: list[int] or comma-separated string
                A comma-separated list of priority IDs to filter by.
            :key refs: str
                A single Reference ID (e.g. TR-1, 4291, etc.)
                (requires TestRail 6.5.2 or later)
            :key section_id: int
                The ID of a test case section
            :key template_id: list[int] or comma-separated string
                A comma-separated list of template IDs to filter by
                (requires TestRail 5.2 or later)
            :key type_id: list[int] or comma-separated string
                A comma-separated list of case type IDs to filter by.
            :key updated_after: int/datetime
                Only return test cases updated after this date (as UNIX timestamp).
            :key updated_before: int/datetime
                Only return test cases updated before this date (as UNIX timestamp).
            :key updated_by: list[int] or comma-separated string
                A comma-separated list of user IDs who updated test cases to filter by.
        :return: response
        """
        return self.s.get(endpoint=f"get_cases/{project_id}", params=kwargs)

    def get_history_for_case(self, case_id: int, limit: int = 250, offset: int = 0) -> list[dict]:
        """
        Returns the edit history for a test case_id.

        Requires TestRail 6.5.4 or later.

        :param case_id int
            The ID of the test case
        :param limit int
            The number of test cases the response should return
            (The response size is 250 by default) (requires TestRail 6.7 or later)
        :param offset int
            Where to start counting the tests cases from (the offset)
            (requires TestRail 6.7 or later)
        """
        return self.s.get(
            endpoint=f"get_history_for_case/{case_id}",
            params={"limit": limit, "offset": offset},
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
        return self.s.post(endpoint=f"add_case/{section_id}", json=dict(title=title, **kwargs))

    def update_case(self, case_id: int, **kwargs) -> dict:
        """
        Updates an existing test case.

        (partial updates are supported, i.e. you can submit and update specific fields only).

        :param case_id: T
            he ID of the test case
        :param kwargs:
            :key title: str
                The title of the test case
            :key section_id: int
                The ID of the section (requires TestRail 6.5.2 or later)
            :key template_id: int
                The ID of the template (requires TestRail 5.2 or later)
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
        return self.s.post(endpoint=f"update_case/{case_id}", json=kwargs)

    def update_cases(self, case_ids: list[int], suite_id: int, **kwargs) -> dict:
        """
        Updates multiple test cases with the same values, such as setting a set of test cases to High priority.

        This does not support updating multiple test cases with different values per test case.

        Note: The online documentation is wrong. The suite_id is required in
        single suite mode as well.

        :param suite_id:
            The ID of the suite
        :param case_ids: list[int]
            The IDs of the test cases to update with the kwargs
        :param kwargs:
            :key title: str
                The title of the test case
            :key section_id: int
                The ID of the section (requires TestRail 6.5.2 or later)
            :key template_id: int
                The ID of the template (requires TestRail 5.2 or later)
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
        """
        kwargs.update({"case_ids": case_ids})
        return self.s.post(endpoint=f"update_cases/{suite_id}", json=kwargs)

    def delete_case(self, case_id: int, soft: int = 0) -> Optional[dict]:
        """
        Deletes an existing test case.

        :param case_id:
            The ID of the test case
        :param soft:
            If soft=1, this will return data on the number of affected tests.
            Including soft=1 will not actually delete the entity.
            Omitting the soft parameter, or submitting soft=0 will delete the test case.
        :return: response
        """
        return self.s.post(endpoint=f"delete_case/{case_id}", params={"soft": soft})

    def delete_cases(
        self,
        project_id: int,
        case_ids: list[int],
        suite_id: Optional[int] = None,
        soft: int = 0,
    ) -> None:
        """
        Deletes multiple test cases from a project or test suite.

        :param project_id:
            The ID of the project
        :param case_ids:
            The case ids to be deleted
        :param suite_id:
            The ID of the suite (Only required if project is in multi-suite mode)
        :param soft:
            Optional parameter
            If soft=1, this will return data on the number of affected tests.
            Including soft=1 will not actually delete the entity.
            Omitting the soft parameter, or submitting soft=0 will delete the test case.
        """
        return self.s.post(
            endpoint=f"delete_cases/{suite_id}" if suite_id else "delete_cases",
            params={"soft": soft, "project_id": project_id},
            json={"case_ids": case_ids},
        )

    def copy_cases_to_section(self, section_id: int, case_ids: list[int]) -> dict:
        """
        Copies the list of cases to another suite/section.

        :param section_id: int
            The ID of the section the test case should be copied to
        :param case_ids:
            List of case IDs.
        """
        return self.s.post(
            endpoint=f"copy_cases_to_section/{section_id}",
            json={"case_ids": ",".join(map(str, case_ids))},
        )

    def move_cases_to_section(self, section_id: int, suite_id: int, case_ids: list[str]) -> dict:
        """
        Moves cases to another suite or section.

        :param section_id: int
            The ID of the section the cases will be moved to.
        :param suite_id: int
            The ID of the suite for the section the cases will be moved to.
        :param case_ids:
            List of case IDs.
        """
        return self.s.post(
            endpoint=f"move_cases_to_section/{section_id}",
            json={
                "case_ids": ",".join(map(str, case_ids)),
                "suite_id": suite_id,
            },
        )

    def get_cases_bulk(self, project_id: int, **kwargs) -> list[dict]:
        """
        Return a list of test cases for a project or specific test suite with pagination.

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
            :key created_by: list[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key filter: str
                Only return cases with matching filter string in the case title
            :key limit: int
                The number of test cases the response should return
                (The response size is 250 by default) (requires TestRail 6.7 or later)
            :key milestone_id: list[int] or comma-separated string
                A comma-separated list of milestone IDs to filter by (not available
                if the milestone field is disabled for the project).
            :key offset: int
                Where to start counting the tests cases from (the offset)
                (requires TestRail 6.7 or later)
            :key priority_id: list[int] or comma-separated string
                A comma-separated list of priority IDs to filter by.
            :key refs: str
                A single Reference ID (e.g. TR-1, 4291, etc.)
                (requires TestRail 6.5.2 or later)
            :key section_id: int
                The ID of a test case section
            :key template_id: list[int] or comma-separated string
                A comma-separated list of template IDs to filter by
                (requires TestRail 5.2 or later)
            :key type_id: list[int] or comma-separated string
                A comma-separated list of case type IDs to filter by.
            :key updated_after: int/datetime
                Only return test cases updated after this date (as UNIX timestamp).
            :key updated_before: int/datetime
                Only return test cases updated before this date (as UNIX timestamp).
            :key updated_by: list[int] or comma-separated string
                A comma-separated list of user IDs who updated test cases to filter by.
        :return: List of test cases
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_cases, "cases", project_id, **kwargs)


class CaseFields(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/case-fields."""

    def get_case_fields(self) -> list[dict]:
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
        return self.s.get(endpoint="get_case_fields")

    def add_case_field(self, type: str, name: str, label: str, configs: list[dict], **kwargs) -> dict:
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
        :param configs:
            An object wrapped in an array with two default keys,
            'context' and 'options' (required)
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
        :return: response
        """
        return self.s.post(
            endpoint="add_case_field",
            json=dict(type=type, name=name, label=label, configs=configs, **kwargs),
        )


class CaseTypes(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/case-types."""

    def get_case_types(self) -> list[dict]:
        """
        Returns a list of available case types.

        The response includes an array of test case types.
        Each case type has a unique ID and a name.
        The is_default field is true for the default case type and false otherwise.

        :return: response
        """
        return self.s.get(endpoint="get_case_types")


class Configurations(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/configurations."""

    def get_configs(self, project_id: int) -> list[dict]:
        """
        Returns a list of available configurations, grouped by configuration groups.

        :param project_id:
            The ID of the project
        :return: response
        """
        return self.s.get(endpoint=f"get_configs/{project_id}")

    def add_config_group(self, project_id: int, name: str) -> dict:
        """
        Creates a new configuration group (requires TestRail 5.2 or later).

        :param project_id:
            The ID of the project the configuration group should be added to
        :param name:
            The name of the configuration group (required)
        :return: response
        """
        return self.s.post(endpoint=f"add_config_group/{project_id}", json={"name": name})

    def add_config(self, config_group_id: int, name: str) -> dict:
        """
        Creates a new configuration (requires TestRail 5.2 or later).

        :param config_group_id:
            The ID of the configuration group the configuration should be added to
        :param name:
            The name of the configuration (required)
        :return: response
        """
        return self.s.post(endpoint=f"add_config/{config_group_id}", json={"name": name})

    def update_config_group(self, config_group_id: int, name: str) -> dict:
        """
        Updates an existing configuration group (requires TestRail 5.2 or later).

        :param config_group_id:
            The ID of the configuration group
        :param name:
            The name of the configuration group
        :return: response
        """
        return self.s.post(
            endpoint=f"update_config_group/{config_group_id}",
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
        return self.s.post(endpoint=f"update_config/{config_id}", json={"name": name})

    def delete_config_group(self, config_group_id: int) -> None:
        """
        Deletes an existing configuration group and its configurations (requires TestRail 5.2 or later).

        :param config_group_id:
            The ID of the configuration group
        :return: response
        """
        return self.s.post(endpoint=f"delete_config_group/{config_group_id}")

    def delete_config(self, config_id: int) -> None:
        """
        Deletes an existing configuration (requires TestRail 5.2 or later).

        :param config_id:
            The ID of the configuration
        :return: response
        """
        return self.s.post(endpoint=f"delete_config/{config_id}")


class Milestones(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/milestones."""

    def get_milestone(self, milestone_id: int) -> dict:
        """
        Returns an existing milestone.

        :param milestone_id:
            The ID of the milestone
        :return: response
        """
        return self.s.get(endpoint=f"get_milestone/{milestone_id}")

    def get_milestones(self, project_id: int, limit: int = 250, offset: int = 0, **kwargs) -> dict:
        """
        Returns the list of milestones for a project.

        :param project_id:
            The ID of the project
        :param limit:
            The number of milestones the response should return
            (The response size is 250 by default) (requires TestRail 6.7 or later)
        :param offset:
            Where to start counting the milestones from (the offset)
            (requires TestRail 6.7 or later)
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
        return self.s.get(
            endpoint=f"get_milestones/{project_id}",
            params=dict(limit=limit, offset=offset, **kwargs),
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
        return self.s.post(endpoint=f"add_milestone/{project_id}", json=dict(name=name, **kwargs))

    def update_milestone(self, milestone_id: int, **kwargs) -> dict:
        """
        Updates an existing milestone.

        (partial updates are supported, i.e. you can submit and update specific fields only).

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
        return self.s.post(endpoint=f"update_milestone/{milestone_id}", json=kwargs)

    def delete_milestone(self, milestone_id: int) -> None:
        """
        Deletes an existing milestone.

        :param milestone_id:
            The ID of the milestone
        :return: response
        """
        return self.s.post(endpoint=f"delete_milestone/{milestone_id}")

    def get_milestones_bulk(self, project_id: int, **kwargs) -> list[dict]:
        """
        Return a list of milestones for a project handling pagination.

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
        return _bulk_api_method(self.get_milestones, "milestones", project_id, **kwargs)


class Plans(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/plans."""

    def get_plan(self, plan_id: int) -> dict:
        """
        Returns an existing test plan.

        :param plan_id:
            The ID of the test plan
        :return: response
        """
        return self.s.get(endpoint=f"get_plan/{plan_id}")

    def get_plans(self, project_id: int, **kwargs) -> dict:
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
            :key created_by: list[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key is_completed: int/bool
                1/True to return completed test plans only.
                0/False to return active test plans only.
            :key limit/offset: int
                Limit the result to :limit test plans. Use :offset to skip records.
            :key milestone_id: list[int] or comma-separated string
                A comma-separated list of milestone IDs to filter by.
        :return: response
        """
        return self.s.get(endpoint=f"get_plans/{project_id}", params=kwargs)

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
        return self.s.post(endpoint=f"add_plan/{project_id}", json=dict(name=name, **kwargs))

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
        return self.s.post(endpoint=f"add_plan_entry/{plan_id}", json=dict(suite_id=suite_id, **kwargs))

    def add_run_to_plan_entry(self, plan_id: int, entry_id: int, config_ids: list[int], **kwargs) -> dict:
        """
        Adds a new test run to a test plan entry (using configurations).

        Requires TestRail 6.4 or later.

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
            :key case_ids: list[int]
                An array of case IDs for the custom case selection
                (Required if include_all is false)
            :key refs: str
                A comma-separated list of references/requirements
        :return: response
        """
        return self.s.post(
            endpoint=f"add_run_to_plan_entry/{plan_id}/{entry_id}",
            json=dict(config_ids=config_ids, **kwargs),
        )

    def update_plan(self, plan_id: int, **kwargs) -> dict:
        """
        Updates an existing test plan.

        (partial updates are supported, i.e. you can submit and update specific fields only).

        :param plan_id:
            The ID of the test plan
        :param kwargs:
            :key name: str
                The name of the test plan
            :key description: str
                The description of the test plan
            :key milestone_id: int
                The ID of the milestone to link to the test plan
            :key entries: list
                An array of objects describing the test runs of the plan, see the
                example below and add_plan_entry
        :return: response
        """
        return self.s.post(endpoint=f"update_plan/{plan_id}", json=kwargs)

    def update_plan_entry(self, plan_id: int, entry_id: int, **kwargs) -> dict:
        """
        Updates one or more existing test runs in a plan.

        (partial updates are supported, i.e. you can submit and update specific fields only).

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
        return self.s.post(endpoint=f"update_plan_entry/{plan_id}/{entry_id}", json=kwargs)

    def update_run_in_plan_entry(self, run_id: int, **kwargs) -> dict:
        """
        Updates a run inside a plan entry which uses configurations requires TestRail 6.4 or later.

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
            :key case_ids: list[int]
                An array of case IDs for the custom case selection.
                (Required if include_all is false)
            :key refs: str
                A comma-separated list of references/requirements
        :return: response
        """
        return self.s.post(endpoint=f"update_run_in_plan_entry/{run_id}", json=kwargs)

    def close_plan(self, plan_id: int) -> dict:
        """
        Closes an existing test plan and archives its test runs & results.

        :param plan_id:
            The ID of the test plan
        :return: response
        """
        return self.s.post(endpoint=f"close_plan/{plan_id}")

    def delete_plan(self, plan_id: int) -> None:
        """
        Deletes an existing test plan.

        :param plan_id:
            The ID of the test plan
        :return: response
        """
        return self.s.post(endpoint=f"delete_plan/{plan_id}")

    def delete_plan_entry(self, plan_id: int, entry_id: int) -> None:
        """
        Deletes one or more existing test runs from a plan.

        :param plan_id:
            The ID of the test plan
        :param entry_id:
            The ID of the test plan entry (note: not the test run ID)
        :return: response
        """
        return self.s.post(endpoint=f"delete_plan_entry/{plan_id}/{entry_id}")

    def delete_run_from_plan_entry(self, run_id: int) -> dict:
        """
        Deletes a test run from a test plan entry.

        :param run_id:
            The ID of the test run
        :return: response
        """
        return self.s.post(endpoint=f"delete_run_from_plan_entry/{run_id}")

    def get_plans_bulk(self, project_id: int, **kwargs) -> list[dict]:
        """
        Return a list of test plans for a project handling pagination.

        :param project_id:
            The ID of the project
        :param kwargs:
            :key is_completed: int
                True for returning completed test plans and false for uncompleted
                test plans
        :return: response
        """
        return _bulk_api_method(self.get_plans, "plans", project_id, **kwargs)


class Priorities(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/priorities."""

    def get_priorities(self) -> list[dict]:
        """
        Returns a list of available priorities.

        :return: response
        """
        return self.s.get(endpoint="get_priorities")


class Projects(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/projects."""

    def get_project(self, project_id: int) -> dict:
        """
        Returns an existing project.

        :param project_id:
            The ID of the project
        :return: response
        """
        return self.s.get(endpoint=f"get_project/{project_id}")

    def get_projects(self, limit: int = 250, offset: int = 0, **kwargs) -> dict:
        """
        Returns the list of available projects.

        :param limit:
            The number of projects the response should return
            (The response size is 250 by default) (requires TestRail 6.7 or later)
        :param offset:
            Where to start counting the projects from (the offset)
            (requires TestRail 6.7 or later)
        :param kwargs: filter
            :key is_completed: int/bool
                1/True to return completed projects only.
                0/False to return active projects only.
        :return: response
        """
        return self.s.get(endpoint="get_projects", params=dict(limit=limit, offset=offset, **kwargs))

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
        return self.s.post(endpoint="add_project", json=dict(name=name, **kwargs))

    def update_project(self, project_id: int, **kwargs) -> dict:
        """
        Updates an existing project.

        (admin status required; partial updates are supported, i.e. you can submit and update specific fields only).

        :param project_id:
            The ID of the project
        :param kwargs:
            :key name: str
                The name of the project
            :key announcement: str
                The description of the project
            :key show_annoucement: bool
                True if the annoucnement should be displayed on the project's
                overview page and false otherwise
            :key is_completed: bool
                Specifies whether a project is considered completed or not
        :return: response
        """
        return self.s.post(endpoint=f"update_project/{project_id}", json=kwargs)

    def delete_project(self, project_id: int) -> None:
        """
        Deletes an existing project (admin status required).

        :param project_id:
            The ID of the project
        :return: response
        """
        return self.s.post(endpoint=f"delete_project/{project_id}")


class Reports(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/reports."""

    def get_reports(self, project_id: int) -> list[dict]:
        """
        Returns a list of API available reports by project.

        Requires TestRail 5.7 or later.

        :param project_id:
            The ID of the project for which you want a list of API accessible reports
        :return: response
        """
        return self.s.get(endpoint=f"get_reports/{project_id}")

    def run_report(self, report_template_id: int) -> dict:
        """
        Executes the report identified using the report_id parameter and returns URL's for accessing the report.

        Requires TestRail 5.7 or later.

        :param report_template_id:
        :return: response
        """
        return self.s.get(endpoint=f"run_report/{report_template_id}")


class Results(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/results."""

    def get_results(self, test_id: int, limit: int = 250, offset: int = 0, **kwargs) -> dict:
        """
        Returns a list of test results for a test.

        :param test_id:
            The ID of the test
        :param limit:
            Number that sets the limit of test results to be shown on the response
            (Optional parameter. The response size limit is 250 by default)
            (requires TestRail 6.7 or later)
        :param offset:
            Number that sets the position where the response should start from
            (Optional parameter) (requires TestRail 6.7 or later)
        :param kwargs: filters
            :key defects_filter: str
                A single Defect ID (e.g. TR-1, 4291, etc.)
            :key status_id: list[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self.s.get(
            endpoint=f"get_results/{test_id}",
            params=dict(limit=limit, offset=offset, **kwargs),
        )

    def get_results_for_case(self, run_id: int, case_id: int, limit: int = 250, offset: int = 0, **kwargs) -> dict:
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
        :param limit:
            The number of test results the response should return
            (The response size is 250 by default) (requires TestRail 6.7 or later)
        :param offset:
            Where to start counting the tests results from (the offset)
            (requires TestRail 6.7 or later)
        :param kwargs: filters
            :key defects_filter: str
                A single Defect ID (e.g. TR-1, 4291, etc.)
            :key status_id: list[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self.s.get(
            endpoint=f"get_results_for_case/{run_id}/{case_id}",
            params=dict(limit=limit, offset=offset, **kwargs),
        )

    def get_results_for_run(self, run_id: int, limit: int = 250, offset: int = 0, **kwargs) -> dict:
        """
        Returns a list of test results for a test run.

        This method will return up to 250 entries in the response array.
        To retrieve additional entries, you can make additional requests using
        the offset filter described in the Request filters section below.

        :param run_id:
            The ID of the test run
        :param limit:
            Number that sets the limit of results to be shown on the response
            (Optional parameter. The response size limit is 250 by default)
            (requires TestRail 6.7 or later)
        :param offset:
            Number that sets the position where the response should start from
            (Optional parameter) (requires TestRail 6.7 or later)
        :param kwargs: filters
            :key created_after: int/datetime
                Only return test results created after this date.
            :key created_before: int/datetime
                Only return test results created before this date.
            :key created_by: list[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key defects_filter: str
                A single Defect ID (e.g. TR-1, 4291, etc.)
            :key status_id: list[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self.s.get(
            endpoint=f"get_results_for_run/{run_id}",
            params=dict(limit=limit, offset=offset, **kwargs),
        )

    def add_result(self, test_id: int, **kwargs) -> list[dict]:
        """
        Adds a new test result, comment or assigns a test.

        It's recommended to use add_results instead if you plan to add results for multiple tests.

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

            Custom fields are supported as well and must be submitted with their
            system name, prefixed with 'custom_', e.g.:
                {
                    ...
                    "custom_comment": "This is a custom comment"
                    ...
                }
        :return: response
        """
        return self.s.post(endpoint=f"add_result/{test_id}", json=kwargs)

    def add_result_for_case(self, run_id: int, case_id: int, **kwargs) -> dict:
        """
        Adds a new test result, comment or assigns a test (for a test run and case combination).

        It's recommended to use add_results_for_cases instead if you
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

            Custom fields are supported as well and must be submitted with their
            system name, prefixed with 'custom_', e.g.:
                {
                    ...
                    "custom_comment": "This is a custom comment"
                    ...
                }
        :return: response
        """
        return self.s.post(
            endpoint=f"add_result_for_case/{run_id}/{case_id}",
            json=kwargs,
        )

    def add_results(self, run_id: int, results: list[dict]) -> list[dict]:
        """
        Method expects an array of test results (via the 'results' field, please see below).

        Each test result must specify the test ID and can pass in the same fields as add_result,
        namely all test related system and custom fields.

        Please note that all referenced tests must belong to the same test run.

        :param run_id:
            The ID of the test run the results should be added to
        :param results: list[dict]
            This method expects an array of test results (via the 'results' field,
            please see below).
            Each test result must specify the test ID and can pass in the same fields
            as add_result, namely all test related system and custom fields.

            Please note that all referenced tests must belong to the same test run.
        :return: response
        """
        return self.s.post(endpoint=f"add_results/{run_id}", json={"results": results})

    def add_results_for_cases(self, run_id: int, results: list[dict]) -> list[dict]:
        """
        Adds one or more new test results, comments or assigns one or more tests (using the case IDs).

        Ideal for test automation to bulk-add multiple test results in one step.
        Requires TestRail 3.1 or later.

        :param run_id:
            The ID of the test run the results should be added to
        :param results: list[dict]
            This method expects an array of test results (via the 'results' field,
            please see below). Each test result must specify the test case ID and
            can pass in the same fields as add_result, namely all test related
            system and custom fields.

            The difference to add_results is that this method expects test case IDs
            instead of test IDs. Please see add_result_for_case for details.

            Please note that all referenced tests must belong to the same test run.
        :return: response
        """
        return self.s.post(
            endpoint=f"add_results_for_cases/{run_id}",
            json={"results": results},
        )

    def get_results_bulk(self, test_id: int, **kwargs) -> list[dict]:
        """
        Return a list of test results for a test run handling pagination.

        :param test_id:
            The ID of the test run
        :param kwargs: filters
            :key defects_filter: str
                A single Defect ID (e.g. TR-1, 4291, etc.)
            :key status_id: list[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: List of results
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_results, "results", test_id, **kwargs)

    def get_results_for_case_bulk(self, run_id: int, case_id: int, **kwargs) -> list[dict]:
        """
        Return a list of test results for a case in a test run handling pagination.

        For the difference between get_results vs get_results_for_case, please see
        the documentation for get_results_for_case.

        :param run_id:
            The ID of the test run
        :param case_id:
            The ID of the test case
        :param kwargs: filters
            :key defects_filter: str
                A single Defect ID (e.g. TR-1, 4291, etc.)
            :key status_id: list[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_results_for_case, "results", run_id, case_id, **kwargs)

    def get_results_for_run_bulk(self, run_id: int, **kwargs) -> list[dict]:
        """
        Returns a list of test results for a test run handling pagination.

        :param run_id:
            The ID of the test run
        :param kwargs: filters
            :key created_after: int/datetime
                Only return test results created after this date.
            :key created_before: int/datetime
                Only return test results created before this date.
            :key created_by: list[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key defects_filter: str
                A single Defect ID (e.g. TR-1, 4291, etc.)
            :key status_id: list[int] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_results_for_run, "results", run_id, **kwargs)


class ResultFields(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/result-fields."""

    def get_result_fields(self) -> list[dict]:
        """
        Returns a list of available test result custom fields.

        :return: response
        """
        return self.s.get(endpoint="get_result_fields")


class Runs(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/runs."""

    def get_run(self, run_id: int) -> dict:
        """
        Returns an existing test run. Please see get_tests for the list of included tests in this run.

        :param run_id:
            The ID of the test run
        :return: response
        """
        return self.s.get(endpoint=f"get_run/{run_id}")

    def get_runs(self, project_id: int, **kwargs) -> dict:
        """
        Returns a list of test runs for a project.

        Only returns those test runs that are not part of a test plan (please see get_plans/get_plan for this).

        :param project_id: int
            The ID of the project
        :param kwargs: filters
            :key created_after: int/datetime
                Only return test runs created after this date (as UNIX timestamp).
            :key created_before: int/datetime
                Only return test runs created before this date (as UNIX timestamp).
            :key created_by: list[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key is_completed: int/bool
                1/True to return completed test runs only.
                0/False to return active test runs only.
            :key limit/offset: int
                Limit the result to :limit test runs. Use :offset to skip records.
            :key milestone_id: list[int] or comma-separated string
                A comma-separated list of milestone IDs to filter by.
            :key refs_filter: str
                A single Reference ID (e.g. TR-a, 4291, etc.)
            :key suite_id: list[int] or comma-separated string
                A comma-separated list of test suite IDs to filter by.
        :return: response
        """
        return self.s.get(endpoint=f"get_runs/{project_id}", params=kwargs)

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
        return self.s.post(endpoint=f"add_run/{project_id}", json=kwargs)

    def update_run(self, run_id: int, **kwargs) -> dict:
        """
        Updates an existing test run.

        (partial updates are supported, i.e. you can submit and update specific fields only).

        :param run_id:
            The ID of the test run
        :param kwargs:
            :key name: str
                The name of the test run
            :key description: str
                The description of the test run
            :key milestone_id: int
                The ID of the milestone to link to the test run
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
        return self.s.post(endpoint=f"update_run/{run_id}", json=kwargs)

    def close_run(self, run_id: int) -> Optional[dict]:
        """
        Closes an existing test run and archives its tests & results.

        Closing a test run cannot be undone.

        :param run_id:
            The ID of the test run
        :return: response
        """
        return self.s.post(endpoint=f"close_run/{run_id}")

    def delete_run(self, run_id: int, soft: int = 0) -> Optional[dict]:
        """
        Deletes an existing test run.

        Deleting a test run cannot be undone and also permanently deletes all
        tests & results of the test run.

        :param run_id:
            The ID of the test run
        :param soft:
            Deleting a test run cannot be undone and also permanently deletes
            all tests & results of the test run.
            Omitting the soft parameter, or submitting soft=0 will delete the test
            run and its tests.
        :return: response
        """
        return self.s.post(endpoint=f"delete_run/{run_id}", params={"soft": soft})

    def get_runs_bulk(self, project_id: int, **kwargs) -> list[dict]:
        """
        Returns a list of test runs for a project.

        Only returns those test runs that are not part of a test plan (please see get_plans/get_plan for this).

        :param project_id: int
            The ID of the project
        :param kwargs: filters
            :key created_after: int/datetime
                Only return test runs created after this date (as UNIX timestamp).
            :key created_before: int/datetime
                Only return test runs created before this date (as UNIX timestamp).
            :key created_by: list[int] or comma-separated string
                A comma-separated list of creators (user IDs) to filter by.
            :key is_completed: int/bool
                1/True to return completed test runs only.
                0/False to return active test runs only.
            :key milestone_id: list[int] or comma-separated string
                A comma-separated list of milestone IDs to filter by.
            :key refs_filter: str
                A single Reference ID (e.g. TR-a, 4291, etc.)
            :key suite_id: list[int] or comma-separated string
                A comma-separated list of test suite IDs to filter by.
        :return: List of runs
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_runs, "runs", project_id, **kwargs)


class Sections(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/sections."""

    def get_section(self, section_id: int) -> dict:
        """
        Returns an existing section.

        :param section_id:
            The ID of the section
        :return: response
        """
        return self.s.get(endpoint=f"get_section/{section_id}")

    def get_sections(self, project_id: int, limit: int = 250, offset: int = 0, **kwargs) -> dict:
        """
        Returns a list of sections for a project and test suite.

        :param project_id:
            The ID of the project
        :param limit: int
                The number of sections the response should return
                (The response size is 250 by default) (requires TestRail 6.7 or later)
        :param offset: int
            Where to start counting the sections from (the offset)
            (requires TestRail 6.7 or later)
        :param kwargs:
            :key suite_id:
                The ID of the test suite (optional if the project is operating in
                single suite mode)
        :return: response
        """
        return self.s.get(
            endpoint=f"get_sections/{project_id}",
            params=dict(limit=limit, offset=offset, **kwargs),
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
        return self.s.post(endpoint=f"add_section/{project_id}", json=dict(name=name, **kwargs))

    def move_section(self, section_id: int, parent_id: int = 0, after_id: Optional[int] = None) -> dict:
        """
        Moves a section to another suite or section (Requires TestRail 6.5.2 or later).

        :param section_id:
            The ID of the section.
        :param parent_id: int
            The ID of the parent section
            (it can be null if it should be moved to the root).
            Must be in the same project and suite.
            May not be direct child of the section being moved.
        :param after_id: int
            The section ID after which the section should be put (can be null)
        """
        return self.s.post(
            endpoint=f"move_section/{section_id}",
            json={"parent_id": parent_id, "after_id": after_id},
        )

    def update_section(self, section_id: int, **kwargs) -> dict:
        """
        Updates an existing section.

        (partial updates are supported, i.e. you can submit and update specific fields only).

        :param section_id:
            The ID of the section
        :param kwargs:
            :key name: str
                The name of the section
            :key description: str
                The description of the section
        :return: response
        """
        return self.s.post(endpoint=f"update_section/{section_id}", json=kwargs)

    def delete_section(self, section_id: int, soft: int = 0) -> None:
        """
        Deletes an existing section.

        :param section_id:
            The ID of the section
        :param soft:
            Deleting a section cannot be undone and also deletes all related test
            cases as well as active tests & results, i.e. tests & results that
            weren't closed (archived) yet.
            Omitting the soft parameter, or submitting soft=0 will delete the
            section and its test cases
        :return: response
        """
        return self.s.post(endpoint=f"delete_section/{section_id}", params={"soft": soft})

    def get_sections_bulk(self, project_id: int, **kwargs) -> list[dict]:
        """
        Returns a list of sections for a project and/or test suite handling pagination.

        :param project_id:
            The ID of the project
        :param kwargs:
            :key suite_id:
                The ID of the test suite (optional if the project is operating in
                single suite mode)
        :return: List of sections
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_sections, "sections", project_id, **kwargs)


class Statuses(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/statuses."""

    def get_statuses(self) -> list[dict]:
        """
        Returns a list of available test statuses.

        :return: response
        """
        return self.s.get(endpoint="get_statuses")

    def get_case_statuses(self) -> list[dict]:
        """
        Returns a list of available test case statuses.

        :return: response
        """
        return self.s.get(endpoint="get_case_statuses")


class Suites(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/suites."""

    def get_suite(self, suite_id: int) -> dict:
        """
        Returns an existing test suite.

        :param suite_id:
            The ID of the test suite
        :return: response
        """
        return self.s.get(endpoint=f"get_suite/{suite_id}")

    def get_suites(self, project_id: int, offset: Optional[int] = None, limit: Optional[int] = None) -> dict:
        """
        Returns a list of test suites for a project.

        :param project_id:
            The ID of the project
        :param offset:
            Where to start counting the suites from the offset.
        :param limit:
            The number of suites the response should return.
        :return: response
        """
        return self.s.get(endpoint=f"get_suites/{project_id}", params=self._opt({"offset": offset, "limit": limit}))

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
        return self.s.post(endpoint=f"add_suite/{project_id}", json=dict(name=name, **kwargs))

    def update_suite(self, suite_id: int, **kwargs) -> dict:
        """
        Updates an existing test suite.

        (partial updates are supported, i.e. you can submit and update specific fields only).

        :param suite_id:
            The ID of the test suite
        :param kwargs:
            :key name: str
                The name of the test suite
            :key description: str
                The description of the test suite
        :return: response
        """
        return self.s.post(endpoint=f"update_suite/{suite_id}", json=kwargs)

    def delete_suite(self, suite_id: int, soft: int = 0) -> None:
        """
        Deletes an existing test suite.

        :param suite_id:
            The ID of the test suite
        :param soft:
            Deleting a test suite cannot be undone and also deletes all active
            test runs & results, i.e. test runs & results that
            weren't closed (archived) yet.
            Omitting the soft parameter, or submitting soft=0 will delete the
            test suite and its test cases
        :return: response
        """
        return self.s.post(endpoint=f"delete_suite/{suite_id}", params={"soft": soft})


class Template(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/templates."""

    def get_templates(self, project_id: int) -> list[dict]:
        """
        Returns a list of available templates (requires TestRail 5.2 or later).

        :param project_id:
            The ID of the project
        :return: response
        """
        return self.s.get(endpoint=f"get_templates/{project_id}")


class Tests(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/tests."""

    def get_test(self, test_id: int, **kwargs) -> dict:
        """
        Returns an existing test.

        If you interested in the test results rather than the tests, please see
        get_results instead.

        :param test_id:
            The ID of the test
        :param kwargs:
            :key with_data:
                The parameter to get data (This is optional)
        :return: response
        """
        return self.s.get(endpoint=f"get_test/{test_id}", params=kwargs)

    def get_tests(self, run_id: int, limit: int = 250, offset: int = 0, **kwargs) -> dict:
        """
        Returns a list of tests for a test run.

        :param run_id:
            The ID of the test run
        :param limit: int
            Number that sets the limit of tests to be shown on the response
            (Optional parameter. The response size limit is 250 by default)
            (requires TestRail 6.7 or later)
        :param offset: int
            Number that sets the position where the response should start from
            (Optional parameter) (requires TestRail 6.7 or later)
        :param kwargs: filters
            :key status_id: list[str] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: response
        """
        return self.s.get(
            endpoint=f"get_tests/{run_id}",
            params=dict(limit=limit, offset=offset, **kwargs),
        )

    def get_tests_bulk(self, run_id: int, **kwargs) -> list[dict]:
        """
        Returns a list of tests for a test run handling pagination.

        :param run_id:
            The ID of the test run
        :param kwargs:
            :key status_id: list[str] or comma-separated string
                A comma-separated list of status IDs to filter by.
        :return: List of tests
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_tests, "tests", run_id, **kwargs)


class Users(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/users."""

    def get_user(self, user_id: int) -> dict:
        """
        Returns an existing user.

        :param user_id:
            The ID of the user
        :return: response
        """
        return self.s.get(endpoint=f"get_user/{user_id}")

    def get_current_user(self, user_id: int) -> dict:
        """
        Returns user details for the TestRail user making the API request (Requires TestRail 6.6 or later).

        :param user_id:
            The ID of the user
        :return: response
        """
        return self.s.get(endpoint=f"get_current_user/{user_id}")

    def get_user_by_email(self, email: str) -> dict:
        """
        Returns an existing user by his/her email address.

        :param email:
            The email address to get the user for
        :return: response
        """
        return self.s.get(endpoint="get_user_by_email", params={"email": email})

    def get_users(
        self, project_id: Optional[int] = None, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> dict:
        """
        Returns a list of users.

        :param project_id:
            The ID of the project for which you would like to retrieve user information.
            (Required for non-administrators. Requires TestRail 6.6 or later.)
        :param offset: int | None
            Where to start counting the users from the offset.
        :param limit: int | None
            The number of users the response should return.
        :return: response
        """
        return self.s.get(
            endpoint=f"get_users/{project_id}" if project_id else "get_users",
            params=self._opt({"offset": offset, "limit": limit}),
        )


class SharedSteps(_MetaCategory):
    """https://www.gurock.com/testrail/docs/api/reference/api-shared-steps."""

    def get_shared_step(self, shared_step_id: int) -> dict:
        """
        Returns an existing set of shared steps.

        :param shared_step_id: int
            The ID of the set of shared steps.
        """
        return self.s.get(endpoint=f"get_shared_step/{shared_step_id}")

    def get_shared_steps(self, project_id: int, **kwargs) -> dict:
        """
        Returns a list of shared steps for a project.

        :param project_id: int
            The ID of the project.
        :param kwargs:
            :key created_after: int or datetime
                Only return shared steps created after this date
            :key created_before: int or datetime
                Only return shared steps created before this date
            :key created_by: list[int] or A comma-separated str
                A comma-separated list of creators (user IDs) to filter by.
            :key limit/offset: int
                Limit the result to :limit test runs. Use :offset to skip records.
            :key updated_after: int or datetime
                Only return shared steps updated after this date
            :key updated_before: int or datetime
                Only return shared steps updated before this date
            :key refs: str
                A single Reference ID (e.g. TR-a, 4291, etc.)
        """
        return self.s.get(endpoint=f"get_shared_steps/{project_id}", params=kwargs)

    def add_shared_step(self, project_id: int, title: str, custom_steps_separated: list[dict]) -> dict:
        """
        Creates a new set of shared steps. Requires permission to add test cases withing the project.

        :param project_id: int
            The ID of the project.
        :param title: int
            The title for the set of steps. (Required)
        :param custom_steps_separated: list
            An array of objects. Each object contains the details for
            an individual step.
            See the table below for more details.

        custom_steps_separated fields:
            additional_info: str: The text contents of the "Additional Info" field.
            content: str: The text contents of the "Step" field.
            expected: str: The text contents of the "Expected Result" field.
            refs: str: Reference information for the "References" field.
        """
        return self.s.post(
            endpoint=f"add_shared_step/{project_id}",
            json={"title": title, "custom_steps_separated": custom_steps_separated},
        )

    def update_shared_step(self, shared_update_id: int, **kwargs) -> dict:
        """
        Updates an existing set of shared steps.

        (partial updates are supported, i.e. you can submit and update specific fields only).

        Requires permission to edit test cases within the project.

        :param shared_update_id: int
            The ID of the set of shared steps.
        :param kwargs:
            :key title: int
                The title for the set of steps.
            :key custom_steps_separated: list
                An array of objects. Each object contains the details for
                an individual step. See the table below for more details.
        """
        return self.s.post(endpoint=f"update_shared_step/{shared_update_id}", json=kwargs)

    def delete_shared_step(self, shared_update_id: int, keep_in_cases: int = 1) -> dict:
        """
        Deletes an existing shared step entity.

        Requires permission to delete test cases within the project.

        :param shared_update_id: int
            The ID of the set of shared steps.
        :param keep_in_cases: int
            Default is 1 (true). Submit keep_in_cases=0 to delete the shared steps from
            all test cases as well as the shared step repository.
        """
        return self.s.post(
            endpoint=f"delete_shared_step/{shared_update_id}",
            json={"keep_in_cases": keep_in_cases},
        )

    def get_shared_steps_bulk(self, project_id: int, **kwargs) -> list[dict]:
        """
        Returns a list of shared steps for a project.

        :param project_id: int
            The ID of the project.
        :param kwargs:
            :key created_after: int or datetime
                Only return shared steps created after this date
            :key created_before: int or datetime
                Only return shared steps created before this date
            :key created_by: list[int] or A comma-separated str
                A comma-separated list of creators (user IDs) to filter by.
            :key updated_after: int or datetime
                Only return shared steps updated after this date
            :key updated_before: int or datetime
                Only return shared steps updated before this date
            :key refs: str
                A single Reference ID (e.g. TR-a, 4291, etc.)
        :return: List of shared steps
        :returns: list[dict]
        """
        return _bulk_api_method(self.get_shared_steps, "shared_steps", project_id, **kwargs)


class Roles(_MetaCategory):
    """https://support.testrail.com/hc/en-us/articles/7077853258772-Roles."""

    def get_roles(self) -> dict[str, Any]:
        """Returns a list of available roles."""
        return self.s.get(endpoint="get_roles")


class Groups(_MetaCategory):
    """https://support.testrail.com/hc/en-us/articles/7077338821012-Groups."""

    def get_group(self, group_id: int) -> dict:
        """
        Returns an existing group.

        :param group_id: int
            The ID of the group
        """
        return self.s.get(f"get_group/{group_id}")

    def get_groups(self) -> dict[str, Any]:
        """Returns the list of available groups."""
        return self.s.get("get_groups")

    def add_group(self, name: str, user_ids: list[int]) -> dict:
        """
        Creates a new group.

        :param name: str
            The name of the group
        :param user_ids: list[int]
            An array of user IDs. Each ID is a user belonging to this group
        """
        return self.s.post("add_group", json={"name": name, "user_ids": user_ids})

    def update_group(self, group_id: int, **kwargs) -> dict:
        """
        Updates an existing group.

        :param group_id: int
            The ID of the group
        :param kwargs:
            :key name: str
                The name of the group
            :key user_ids: list[int]
                An array of user IDs. Each ID is a user belonging to this group
        """
        return self.s.post(f"update_group/{group_id}", json=kwargs)

    def delete_group(self, group_id: int) -> None:
        """
        Deletes an existing group.

        :param group_id: int
            The ID of the group
        """
        return self.s.post(f"delete_group/{group_id}")


class Variables(_MetaCategory):
    """https://support.testrail.com/hc/en-us/articles/7077979742868-Variables."""

    def get_variables(self, project_id: int) -> dict:
        """
        Retrieves the requested variables.

        :param project_id: int
            The ID of the project from which to retrieve variables.
        """
        return self.s.get(endpoint=f"get_variables/{project_id}")

    def add_variable(self, project_id: int, id: int, name: str) -> dict:
        """
        Creates a new variable.

        :param project_id: int
            The ID of the project to which the variable should be added.
        :param id: int
            The ID of the newly added variable
        :param name: str
            Name of the newly added variable
        """
        return self.s.post(endpoint=f"add_variable/{project_id}", json={"name": name, "id": id})

    def update_variable(self, variable_id: int, name: str) -> dict:
        """
        Updates an existing variable.

        :param variable_id: int
            The ID of the variable to update.
        :param name: str
            Name of the variable to update
        """
        return self.s.post(endpoint=f"update_variable/{variable_id}", json={"name": name})

    def delete_variable(self, variable_id: int) -> None:
        """
        Deletes an existing variable.

        :param variable_id: str
            The ID of the variable to be deleted.
        """
        return self.s.post(endpoint=f"delete_variable/{variable_id}")


class Datasets(_MetaCategory):
    """https://support.testrail.com/hc/en-us/articles/7077300491540-Datasets."""

    def get_dataset(self, dataset_id: int) -> dict:
        """
        Retrieves the requested dataset parameter.

        :param dataset_id: int
            The ID of the dataset to retrieve
        """
        return self.s.get(endpoint=f"get_dataset/{dataset_id}")

    def get_datasets(self, project_id: int) -> dict:
        """
        Retrieves the requested list of datasets.

        :param project_id: int
            The ID of the project from which to retrieve datasets
        """
        return self.s.get(endpoint=f"get_datasets/{project_id}")

    def add_dataset(self, project_id: int, id: int, name: str, variables: list[dict]) -> dict:
        """
        Creates a new dataset.

        :param project_id: int
            The ID of the project to which the dataset should be added
        :param id: int
            The database ID of the dataset
        :param name: str
            Name of the dataset as provided
        :param variables: list[dict]
            Key/Value pairs. Key should be the variable name. Value should be the value to be included in the dataset.
        """
        return self.s.post(endpoint=f"add_dataset/{project_id}", json={"name": name, "variables": variables, "id": id})

    def update_dataset(self, dataset_id: int, **kwargs) -> dict:
        """
        Updates an existing dataset.

        :param dataset_id: int
            The ID of the project to which the dataset should be updated
        :param kwargs:
            :key name: str
                Name of the dataset as provided
            :key variables: list[dict]
                Key/Value pairs. Key should be the variable name.
        """
        return self.s.post(endpoint=f"update_dataset/{dataset_id}", json=kwargs)

    def delete_dataset(self, dataset_id: int) -> None:
        """
        Deletes an existing dataset.Parameter.

        :param dataset_id: int
            The ID of the dataset to be deleted
        """
        return self.s.post(endpoint=f"delete_dataset/{dataset_id}")


class Labels(_MetaCategory):
    """https://support.testrail.com/hc/en-us/articles/38961149782036-Labels."""

    def get_labels(self, project_id: int, offset: Optional[int] = None, limit: Optional[int] = None) -> dict:
        """
        Returns an existing label.

        :param project_id: int
            The ID of the project.
        :param offset: int | None
            Where to start counting the test cases from the offset.
        :param limit: int | None
            The number of labels the response should return.
        """
        return self.s.get(endpoint=f"get_labels/{project_id}", params=self._opt({"offset": offset, "limit": limit}))

    def get_label(self, label_id: int) -> dict:
        """
        Returns an existing label.

        :param label_id: int
            Returns an existing label.
        """
        return self.s.get(endpoint=f"get_label/{label_id}")

    def update_label(self, label_id: int, project_id: int, title: str) -> dict:
        """
        Updates an existing label.

        :param label_id: int
            The ID of the label to update.
        :param project_id: int
            The ID of the project where the label is to be updated.
        :param title: str
            The title of the label. Maximum 20 characters allowed.
        """
        return self.s.post(endpoint=f"update_label/{label_id}", json={"title": title, "project_id": project_id})
