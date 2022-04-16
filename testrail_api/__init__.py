# -*- coding: utf-8 -*-

"""
Python wrapper of the TestRail API

------------------
from datetime import datetime

from testrail_api import TestRailAPI

api = TestRailAPI("https://example.testrail.com/", "example@mail.com", "password")

# if use environment variables
# api = TestRailAPI()


new_milestone = api.milestones.add_milestone(
    project_id=1,
    name="New milestone",
    start_on=int(datetime.now().timestamp())
)

my_test_run = api.runs.add_run(
    project_id=1,
    suite_id=2,
    name="My test run",
    include_all=True,
    milestone_id=new_milestone["id"]
)

result = api.results.add_result_for_case(
    run_id=my_test_run["id"],
    case_id=5,
    status_id=1,
    comment="Pass",
    version="1"
)
attach = "attach.jpg"
api.attachments.add_attachment_to_result(result["id"], attach)

api.runs.close_run(my_test_run["id"])
api.milestones.update_milestone(new_milestone["id"], is_completed=True)
------------------
"""

try:
    from .__version__ import version as __version__
except ImportError:  # pragma: no cover
    __version__ = "unknown"

import logging
import sys
import warnings

from ._exception import StatusCodeError
from ._testrail_api import TestRailAPI

if (sys.version_info.major, sys.version_info.minor) < (3, 6):  # pragma: no cover
    warnings.warn(
        "Python 3.5 support will be removed in testrail-api 1.11.0",
        PendingDeprecationWarning,
    )

logging.getLogger(__package__).addHandler(logging.NullHandler())

__all__ = ["TestRailAPI", "StatusCodeError", "__version__"]
