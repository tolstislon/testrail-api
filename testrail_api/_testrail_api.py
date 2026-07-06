"""TestRail API Categories."""

from functools import cached_property

from . import _category
from ._session import Session


class TestRailAPI(Session):
    """
    API Categories.

    Each category is exposed as a cached property bound to this instance's session.
    Binding per instance (instead of a shared descriptor) keeps categories isolated
    across multiple ``TestRailAPI`` objects and threads.
    """

    @cached_property
    def attachments(self) -> _category.Attachments:
        """Attachments category."""
        return _category.Attachments(self)

    @cached_property
    def bdds(self) -> _category.Bdds:
        """Bdds category."""
        return _category.Bdds(self)

    @cached_property
    def cases(self) -> _category.Cases:
        """Cases category."""
        return _category.Cases(self)

    @cached_property
    def case_fields(self) -> _category.CaseFields:
        """CaseFields category."""
        return _category.CaseFields(self)

    @cached_property
    def case_types(self) -> _category.CaseTypes:
        """CaseTypes category."""
        return _category.CaseTypes(self)

    @cached_property
    def configurations(self) -> _category.Configurations:
        """Configurations category."""
        return _category.Configurations(self)

    @cached_property
    def milestones(self) -> _category.Milestones:
        """Milestones category."""
        return _category.Milestones(self)

    @cached_property
    def plans(self) -> _category.Plans:
        """Plans category."""
        return _category.Plans(self)

    @cached_property
    def priorities(self) -> _category.Priorities:
        """Priorities category."""
        return _category.Priorities(self)

    @cached_property
    def projects(self) -> _category.Projects:
        """Projects category."""
        return _category.Projects(self)

    @cached_property
    def reports(self) -> _category.Reports:
        """Reports category."""
        return _category.Reports(self)

    @cached_property
    def results(self) -> _category.Results:
        """Results category."""
        return _category.Results(self)

    @cached_property
    def result_fields(self) -> _category.ResultFields:
        """ResultFields category."""
        return _category.ResultFields(self)

    @cached_property
    def runs(self) -> _category.Runs:
        """Runs category."""
        return _category.Runs(self)

    @cached_property
    def sections(self) -> _category.Sections:
        """Sections category."""
        return _category.Sections(self)

    @cached_property
    def shared_steps(self) -> _category.SharedSteps:
        """SharedSteps category."""
        return _category.SharedSteps(self)

    @cached_property
    def statuses(self) -> _category.Statuses:
        """Statuses category."""
        return _category.Statuses(self)

    @cached_property
    def suites(self) -> _category.Suites:
        """Suites category."""
        return _category.Suites(self)

    @cached_property
    def templates(self) -> _category.Template:
        """Template category."""
        return _category.Template(self)

    @cached_property
    def tests(self) -> _category.Tests:
        """Tests category."""
        return _category.Tests(self)

    @cached_property
    def users(self) -> _category.Users:
        """Users category."""
        return _category.Users(self)

    @cached_property
    def roles(self) -> _category.Roles:
        """Roles category."""
        return _category.Roles(self)

    @cached_property
    def groups(self) -> _category.Groups:
        """Groups category."""
        return _category.Groups(self)

    @cached_property
    def variables(self) -> _category.Variables:
        """Variables category."""
        return _category.Variables(self)

    @cached_property
    def datasets(self) -> _category.Datasets:
        """Datasets category."""
        return _category.Datasets(self)

    @cached_property
    def dynamic_filter_fields(self) -> _category.DynamicFilterFields:
        """DynamicFilterFields category."""
        return _category.DynamicFilterFields(self)

    @cached_property
    def labels(self) -> _category.Labels:
        """Labels category."""
        return _category.Labels(self)
