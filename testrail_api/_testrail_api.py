"""TestRail API Categories."""

from . import _category
from ._session import Session


class TestRailAPI(Session):
    """API Categories."""

    attachments: _category.Attachments = _category.Attachments()
    cases: _category.Cases = _category.Cases()
    case_fields: _category.CaseFields = _category.CaseFields()
    case_types: _category.CaseTypes = _category.CaseTypes()
    configurations: _category.Configurations = _category.Configurations()
    milestones: _category.Milestones = _category.Milestones()
    plans: _category.Plans = _category.Plans()
    priorities: _category.Priorities = _category.Priorities()
    projects: _category.Projects = _category.Projects()
    reports: _category.Reports = _category.Reports()
    results: _category.Results = _category.Results()
    result_fields: _category.ResultFields = _category.ResultFields()
    runs: _category.Runs = _category.Runs()
    sections: _category.Sections = _category.Sections()
    shared_steps: _category.SharedSteps = _category.SharedSteps()
    statuses: _category.Statuses = _category.Statuses()
    suites: _category.Suites = _category.Suites()
    templates: _category.Template = _category.Template()
    tests: _category.Tests = _category.Tests()
    users: _category.Users = _category.Users()
    roles: _category.Roles = _category.Roles()
    groups: _category.Groups = _category.Groups()
    variables: _category.Variables = _category.Variables()
    datasets: _category.Datasets = _category.Datasets()
    labels: _category.Labels = _category.Labels()
