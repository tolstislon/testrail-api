class TestRailError(Exception):
    """Base Exception"""
    pass


class TestRailAPIError(TestRailError):
    pass


class StatusCodeError(TestRailAPIError):
    pass
