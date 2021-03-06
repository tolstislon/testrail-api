"""
TestRail API Categories
"""

from . import _category
from ._session import Session


class TestRailAPI(Session):
    """Categories"""

    @property
    def attachments(self) -> _category.Attachments:
        """
        https://www.gurock.com/testrail/docs/api/reference/attachments
        Use the following API methods to upload, retrieve and delete attachments.
        """
        return _category.Attachments(self)

    @property
    def cases(self) -> _category.Cases:
        """
        https://www.gurock.com/testrail/docs/api/reference/cases
        Use the following API methods to request details about test cases and
        to create or modify test cases.
        """
        return _category.Cases(self)

    @property
    def case_fields(self) -> _category.CaseFields:
        """
        https://www.gurock.com/testrail/docs/api/reference/case-fields
        Use the following API methods to request details about custom fields
        for test cases.
        """
        return _category.CaseFields(self)

    @property
    def case_types(self) -> _category.CaseTypes:
        """
        https://www.gurock.com/testrail/docs/api/reference/case-types
        Use the following API methods to request details about case type.
        """
        return _category.CaseTypes(self)

    @property
    def configurations(self) -> _category.Configurations:
        """
        https://www.gurock.com/testrail/docs/api/reference/configurations
        Use the following API methods to request details about configurations and
        to create or modify configurations.
        """
        return _category.Configurations(self)

    @property
    def milestones(self) -> _category.Milestones:
        """
        https://www.gurock.com/testrail/docs/api/reference/milestones
        Use the following API methods to request details about milestones and
        to create or modify milestones.
        """
        return _category.Milestones(self)

    @property
    def plans(self) -> _category.Plans:
        """
        https://www.gurock.com/testrail/docs/api/reference/plans
        Use the following API methods to request details about test plans and
        to create or modify test plans.
        """
        return _category.Plans(self)

    @property
    def priorities(self) -> _category.Priorities:
        """
        https://www.gurock.com/testrail/docs/api/reference/priorities
        Use the following API methods to request details about priorities.
        """
        return _category.Priorities(self)

    @property
    def projects(self) -> _category.Projects:
        """
        https://www.gurock.com/testrail/docs/api/reference/projects
        Use the following API methods to request details about projects and
        to create or modify projects
        """
        return _category.Projects(self)

    @property
    def reports(self) -> _category.Reports:
        """
        https://www.gurock.com/testrail/docs/api/reference/reports
        Use the following methods to get and run reports that have been
        made accessible to the API.
        """
        return _category.Reports(self)

    @property
    def results(self) -> _category.Results:
        """
        https://www.gurock.com/testrail/docs/api/reference/results
        Use the following API methods to request details about test results and
        to add new test results.
        """
        return _category.Results(self)

    @property
    def result_fields(self) -> _category.ResultFields:
        """
        https://www.gurock.com/testrail/docs/api/reference/result-fields
        Use the following API methods to request details about custom fields
        for test results.
        """
        return _category.ResultFields(self)

    @property
    def runs(self) -> _category.Runs:
        """
        https://www.gurock.com/testrail/docs/api/reference/runs
        Use the following API methods to request details about test runs and
        to create or modify test runs.
        """
        return _category.Runs(self)

    @property
    def sections(self) -> _category.Sections:
        """
        https://www.gurock.com/testrail/docs/api/reference/sections
        Use the following API methods to request details about sections and
        to create or modify sections.
        Sections are used to group and organize test cases in test suites.
        """
        return _category.Sections(self)

    @property
    def shared_steps(self) -> _category.SharedSteps:
        """
        https://www.gurock.com/testrail/docs/api/reference/api-shared-steps
        Use the following API methods to request details about shared steps.
        """
        return _category.SharedSteps(self)

    @property
    def statuses(self) -> _category.Statuses:
        """
        https://www.gurock.com/testrail/docs/api/reference/statuses
        Use the following API methods to request details about test statuses.
        """
        return _category.Statuses(self)

    @property
    def suites(self) -> _category.Suites:
        """
        https://www.gurock.com/testrail/docs/api/reference/suites
        Use the following API methods to request details about test suites and
        to create or modify test suites.
        """
        return _category.Suites(self)

    @property
    def templates(self) -> _category.Template:
        """
        https://www.gurock.com/testrail/docs/api/reference/templates
        Use the following API methods to request details about templates
        (field layouts for cases/results)
        """
        return _category.Template(self)

    @property
    def tests(self) -> _category.Tests:
        """
        https://www.gurock.com/testrail/docs/api/reference/tests
        Use the following API methods to request details about tests.
        """
        return _category.Tests(self)

    @property
    def users(self) -> _category.Users:
        """
        https://www.gurock.com/testrail/docs/api/reference/users
        Use the following API methods to request details about users.
        """
        return _category.Users(self)
