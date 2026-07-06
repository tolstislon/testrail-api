"""Enums."""

from enum import Enum, IntEnum


class METHODS(Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"


class ResultStatus(IntEnum):
    """
    Default TestRail result statuses.

    TestRail administrators can define custom statuses (IDs 6+); for those,
    keep passing plain ``int`` values.
    """

    PASSED = 1
    BLOCKED = 2
    UNTESTED = 3
    RETEST = 4
    FAILED = 5


class SuiteMode(IntEnum):
    """Project suite modes (the ``suite_mode`` field of a project)."""

    SINGLE = 1
    SINGLE_WITH_BASELINES = 2
    MULTIPLE = 3
