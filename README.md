![PyPI](https://img.shields.io/pypi/v/testrail-api?color=%2301a001&label=version&logo=version)
[![Downloads](https://pepy.tech/badge/testrail-api)](https://pepy.tech/project/testrail-api)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/testrail-api.svg)
# testrail-api


This is a Python wrapper of the TestRail API(v2) according to [the official document](http://docs.gurock.com/testrail-api2/start)


### Install

```bash
pip install testrail-api
```

### Example

```python
from datetime import datetime
from pathlib import Path

from testrail_api import TestRailAPI

api = TestRailAPI('https://example.testrail.com/', 'example@mail.com', 'password')

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
attach = Path('.', 'attach.jpg')
api.attachments.add_attachment_to_result(result[0]['id'], attach)

api.runs.close_run(my_test_run['id'])
api.milestones.update_milestone(new_milestone['id'], is_completed=True)
```

----

### Last test

* Python: 3.7.4
* TestRail: 6.0.2.4165
* testrail-api: 1.3.5

Coverage:

```bash
Name                            Stmts   Miss  Cover
---------------------------------------------------
testrail_api\__init__.py            5      0   100%
testrail_api\__version__.py         6      0   100%
testrail_api\_category.py         178      0   100%
testrail_api\_enums.py              6      0   100%
testrail_api\_session.py           69      0   100%
testrail_api\_testrail_api.py      57      0   100%
---------------------------------------------------
TOTAL                             321      0   100%
```