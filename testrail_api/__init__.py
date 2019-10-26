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

from .__version__ import (
    __version__,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __url__
)

from ._testrail_api import TestRailAPI
from ._session import StatusCodeError

import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

__all__ = [
    'TestRailAPI',
    '__version__',
    '__author__',
    '__author_email__',
    '__description__',
    '__license__',
    '__url__',
    'StatusCodeError'
]
