# Testrail Api

[![PyPI](https://img.shields.io/pypi/v/testrail-api?color=%2301a001&label=version&logo=version)](https://pypi.org/project/testrail-api/)
[![Downloads](https://pepy.tech/badge/testrail-api)](https://pepy.tech/project/testrail-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/testrail-api.svg)](https://pypi.org/project/testrail-api/)
[![pytes_support](https://img.shields.io/badge/Pypy-3-blue.svg)](https://pypi.org/project/testrail-api/)
[![Build Status](https://travis-ci.com/tolstislon/testrail-api.svg?branch=master)](https://travis-ci.com/tolstislon/testrail-api)
[![codecov](https://codecov.io/gh/tolstislon/testrail-api/branch/master/graph/badge.svg)](https://codecov.io/gh/tolstislon/testrail-api)

This is a Python wrapper of the TestRail API(v2) according to [the official documentation](http://docs.gurock.com/testrail-api2/start)


Install
----

```bash
pip install testrail-api
```

##### Support environment variables
* `TESTRAIL_URL`
* `TESTRAIL_EMAIL`
* `TESTRAIL_PASSWORD`

Example
----
```python
from datetime import datetime

from testrail_api import TestRailAPI

api = TestRailAPI('https://example.testrail.com/', 'example@mail.com', 'password')

# if use environment variables
# api = TestRailAPI()


new_milestone = api.milestones.add_milestone(
    project_id=1, 
    name='New milestone', 
    start_on=int(datetime.now().timestamp())
)

my_test_run = api.runs.add_run(
    project_id=1, 
    suite_id=2, 
    name='My test run', 
    include_all=True, 
    milestone_id=new_milestone['id']
)

result = api.results.add_result_for_case(
    run_id=my_test_run['id'], 
    case_id=5, 
    status_id=1, 
    comment='Pass', 
    version='1'
)
attach = 'attach.jpg'
api.attachments.add_attachment_to_result(result[0]['id'], attach)

api.runs.close_run(my_test_run['id'])
api.milestones.update_milestone(new_milestone['id'], is_completed=True)
```


Contributing
----
Contributions are very welcome.
