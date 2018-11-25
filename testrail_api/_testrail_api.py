"""
Description
"""

from . import _category
from ._session import Session


class TestRailAPI(Session):

    @property
    def cases(self):
        """http://docs.gurock.com/testrail-api2/reference-cases"""
        return _category.Cases(self)

    @property
    def case_fields(self):
        """http://docs.gurock.com/testrail-api2/reference-cases-fields"""
        return _category.CaseFields(self)

    @property
    def case_types(self):
        """http://docs.gurock.com/testrail-api2/reference-cases-types"""
        return _category.CaseTypes(self)

    @property
    def configurations(self):
        """http://docs.gurock.com/testrail-api2/reference-configs"""
        return _category.Configurations(self)

    @property
    def milestones(self):
        """http://docs.gurock.com/testrail-api2/reference-milestones"""
        return _category.Milestones(self)

    @property
    def plans(self):
        """http://docs.gurock.com/testrail-api2/reference-plans"""
        return _category.Plans(self)

    @property
    def priorities(self):
        """http://docs.gurock.com/testrail-api2/reference-priorities"""
        return _category.Priorities(self)

    @property
    def projects(self):
        """http://docs.gurock.com/testrail-api2/reference-projects"""
        return _category.Projects(self)

    @property
    def results(self):
        """http://docs.gurock.com/testrail-api2/reference-results"""
        return _category.Results(self)

    @property
    def result_fields(self):
        """http://docs.gurock.com/testrail-api2/reference-results-fields"""
        return _category.ResultFields(self)

    @property
    def runs(self):
        """http://docs.gurock.com/testrail-api2/reference-runs"""
        return _category.Runs(self)

    @property
    def sections(self):
        """http://docs.gurock.com/testrail-api2/reference-runs"""
        return _category.Sections(self)

    @property
    def statuses(self):
        """http://docs.gurock.com/testrail-api2/reference-sections"""
        return _category.Statuses(self)

    @property
    def suites(self):
        """http://docs.gurock.com/testrail-api2/reference-suites"""
        return _category.Suites(self)

    @property
    def templates(self):
        """http://docs.gurock.com/testrail-api2/reference-templates"""
        return _category.Templates(self)

    @property
    def tests(self):
        """http://docs.gurock.com/testrail-api2/reference-tests"""
        return _category.Tests(self)

    @property
    def users(self):
        """http://docs.gurock.com/testrail-api2/reference-users"""
        return _category.Users(self)
