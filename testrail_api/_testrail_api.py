"""
TestRail API Categories
"""

from . import _category
from ._session import Session


class TestRailAPI(Session):
    """Categories"""

    @property
    def attachments(self) -> _category.Attachments:
        """http://docs.gurock.com/testrail-api2/reference-attachments"""
        return _category.Attachments(self)

    @property
    def cases(self) -> _category.Cases:
        """http://docs.gurock.com/testrail-api2/reference-cases"""
        return _category.Cases(self)

    @property
    def case_fields(self) -> _category.CaseFields:
        """http://docs.gurock.com/testrail-api2/reference-cases-fields"""
        return _category.CaseFields(self)

    @property
    def case_types(self) -> _category.CaseTypes:
        """http://docs.gurock.com/testrail-api2/reference-cases-types"""
        return _category.CaseTypes(self)

    @property
    def configurations(self) -> _category.Configurations:
        """http://docs.gurock.com/testrail-api2/reference-configs"""
        return _category.Configurations(self)

    @property
    def milestones(self) -> _category.Milestones:
        """http://docs.gurock.com/testrail-api2/reference-milestones"""
        return _category.Milestones(self)

    @property
    def plans(self) -> _category.Plans:
        """http://docs.gurock.com/testrail-api2/reference-plans"""
        return _category.Plans(self)

    @property
    def priorities(self) -> _category.Priorities:
        """http://docs.gurock.com/testrail-api2/reference-priorities"""
        return _category.Priorities(self)

    @property
    def projects(self) -> _category.Projects:
        """http://docs.gurock.com/testrail-api2/reference-projects"""
        return _category.Projects(self)

    @property
    def results(self) -> _category.Results:
        """http://docs.gurock.com/testrail-api2/reference-results"""
        return _category.Results(self)

    @property
    def result_fields(self) -> _category.ResultFields:
        """http://docs.gurock.com/testrail-api2/reference-results-fields"""
        return _category.ResultFields(self)

    @property
    def runs(self) -> _category.Runs:
        """http://docs.gurock.com/testrail-api2/reference-runs"""
        return _category.Runs(self)

    @property
    def sections(self) -> _category.Sections:
        """http://docs.gurock.com/testrail-api2/reference-runs"""
        return _category.Sections(self)

    @property
    def statuses(self) -> _category.Statuses:
        """http://docs.gurock.com/testrail-api2/reference-sections"""
        return _category.Statuses(self)

    @property
    def suites(self) -> _category.Suites:
        """http://docs.gurock.com/testrail-api2/reference-suites"""
        return _category.Suites(self)

    @property
    def templates(self) -> _category.Template:
        """http://docs.gurock.com/testrail-api2/reference-templates"""
        return _category.Template(self)

    @property
    def tests(self) -> _category.Tests:
        """http://docs.gurock.com/testrail-api2/reference-tests"""
        return _category.Tests(self)

    @property
    def users(self) -> _category.Users:
        """http://docs.gurock.com/testrail-api2/reference-users"""
        return _category.Users(self)

    @property
    def reports(self) -> _category.Reports:
        """http://docs.gurock.com/testrail-api2/reference-reports"""
        return _category.Reports(self)
