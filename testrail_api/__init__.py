# -*- coding: utf-8 -*-

"""
Python wrapper of the TestRail API

------------------
from testrail_api import TestRailAPI

api = TestRailAPI('https://example.testrail.com/', 'example@mail.com', 'password')
my_case = api.cases.get_case(22)
api.cases.add_case(1, 'New Case', milestone_id=1)
------------------

"""

try:
    from .__version__ import version as __version__
except ImportError:
    __version__ = "unknown"

import logging
from logging import NullHandler

from ._exception import StatusCodeError
from ._testrail_api import TestRailAPI

logging.getLogger(__name__).addHandler(NullHandler())

__all__ = ["TestRailAPI", "StatusCodeError", "__version__"]
