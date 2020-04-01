"""Exceptions"""


class TestRailError(Exception):
    """Base Exception"""


class TestRailAPIError(TestRailError):
    """Base API Exception"""


class StatusCodeError(TestRailAPIError):
    """Status code Exception"""
