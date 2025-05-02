"""TestRail API Categories."""

from . import _category
from ._session import Session


class TestRailAPI(Session):
    """API Categories."""

    @property
    def attachments(self) -> _category.Attachments:
        """
        Use the following API methods to upload, retrieve and delete attachments.

        https://www.gurock.com/testrail/docs/api/reference/attachments
        """
        return _category.Attachments(self)

    @property
    def cases(self) -> _category.Cases:
        """
        Use the following API methods to request details about test cases and to create or modify test cases.

        https://www.gurock.com/testrail/docs/api/reference/cases
        """
        return _category.Cases(self)

    @property
    def case_fields(self) -> _category.CaseFields:
        """
        Use the following API methods to request details about custom fields for test cases.

        https://www.gurock.com/testrail/docs/api/reference/case-fields
        """
        return _category.CaseFields(self)

    @property
    def case_types(self) -> _category.CaseTypes:
        """
        Use the following API methods to request details about case type.

        https://www.gurock.com/testrail/docs/api/reference/case-types
        """
        return _category.CaseTypes(self)

    @property
    def configurations(self) -> _category.Configurations:
        """
        Use the following API methods to request details about configurations and to create or modify configurations.

        https://www.gurock.com/testrail/docs/api/reference/configurations
        """
        return _category.Configurations(self)

    @property
    def milestones(self) -> _category.Milestones:
        """
        Use the following API methods to request details about milestones and to create or modify milestones.

        https://www.gurock.com/testrail/docs/api/reference/milestones
        """
        return _category.Milestones(self)

    @property
    def plans(self) -> _category.Plans:
        """
        Use the following API methods to request details about test plans and to create or modify test plans.

        https://www.gurock.com/testrail/docs/api/reference/plans
        """
        return _category.Plans(self)

    @property
    def priorities(self) -> _category.Priorities:
        """
        Use the following API methods to request details about priorities.

        https://www.gurock.com/testrail/docs/api/reference/priorities
        """
        return _category.Priorities(self)

    @property
    def projects(self) -> _category.Projects:
        """
        Use the following API methods to request details about projects and to create or modify projects.

        https://www.gurock.com/testrail/docs/api/reference/projects
        """
        return _category.Projects(self)

    @property
    def reports(self) -> _category.Reports:
        """
        Use the following methods to get and run reports that have been made accessible to the API.

        https://www.gurock.com/testrail/docs/api/reference/reports
        """
        return _category.Reports(self)

    @property
    def results(self) -> _category.Results:
        """
        Use the following API methods to request details about test results and to add new test results.

        https://www.gurock.com/testrail/docs/api/reference/results
        """
        return _category.Results(self)

    @property
    def result_fields(self) -> _category.ResultFields:
        """
        Use the following API methods to request details about custom fields for test results.

        https://www.gurock.com/testrail/docs/api/reference/result-fields
        """
        return _category.ResultFields(self)

    @property
    def runs(self) -> _category.Runs:
        """
        Use the following API methods to request details about test runs and to create or modify test runs.

        https://www.gurock.com/testrail/docs/api/reference/runs
        """
        return _category.Runs(self)

    @property
    def sections(self) -> _category.Sections:
        """
        Use the following API methods to request details about sections and to create or modify sections.

        Sections are used to group and organize test cases in test suites.
        https://www.gurock.com/testrail/docs/api/reference/sections
        """
        return _category.Sections(self)

    @property
    def shared_steps(self) -> _category.SharedSteps:
        """
        Use the following API methods to request details about shared steps.

        https://www.gurock.com/testrail/docs/api/reference/api-shared-steps
        """
        return _category.SharedSteps(self)

    @property
    def statuses(self) -> _category.Statuses:
        """
        Use the following API methods to request details about test statuses.

        https://www.gurock.com/testrail/docs/api/reference/statuses
        """
        return _category.Statuses(self)

    @property
    def suites(self) -> _category.Suites:
        """
        Use the following API methods to request details about test suites and to create or modify test suites.

        https://www.gurock.com/testrail/docs/api/reference/suites
        """
        return _category.Suites(self)

    @property
    def templates(self) -> _category.Template:
        """
        Use the following API methods to request details about templates (field layouts for cases/results).

        https://www.gurock.com/testrail/docs/api/reference/templates
        """
        return _category.Template(self)

    @property
    def tests(self) -> _category.Tests:
        """
        Use the following API methods to request details about tests.

        https://www.gurock.com/testrail/docs/api/reference/tests
        """
        return _category.Tests(self)

    @property
    def users(self) -> _category.Users:
        """
        Use the following API methods to request details about users.

        https://www.gurock.com/testrail/docs/api/reference/users
        """
        return _category.Users(self)

    @property
    def roles(self) -> _category.Roles:
        """
        Use the following API methods to request details about roles.

        https://support.testrail.com/hc/en-us/articles/7077853258772-Roles
        """
        return _category.Roles(self)

    @property
    def groups(self) -> _category.Groups:
        """
        Use the following API methods to request details about groups.

        https://support.testrail.com/hc/en-us/articles/7077338821012-Groups
        """
        return _category.Groups(self)

    @property
    def variables(self) -> _category.Variables:
        """
        Use the following API methods to upload, retrieve, update, and delete variables that exist in datasets.

        https://support.testrail.com/hc/en-us/articles/7077979742868-Variables
        """
        return _category.Variables(self)

    @property
    def datasets(self) -> _category.Datasets:
        """
        Use the following API methods to upload, retrieve, update, and delete datasets.

        https://support.testrail.com/hc/en-us/articles/7077300491540-Datasets
        """
        return _category.Datasets(self)
