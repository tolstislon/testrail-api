# Testrail Api

[![PyPI](https://img.shields.io/pypi/v/testrail-api?color=%2301a001&label=pypi&logo=version)](https://pypi.org/project/testrail-api/)
[![Downloads](https://pepy.tech/badge/testrail-api)](https://pepy.tech/project/testrail-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/testrail-api.svg)](https://pypi.org/project/testrail-api/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/testrail-api)](https://pypi.org/project/testrail-api/)
[![Build Pypi](https://github.com/tolstislon/testrail-api/actions/workflows/python-publish.yml/badge.svg)](https://github.com/tolstislon/testrail-api)

This is a Python wrapper of the TestRail API according
to [the official documentation](https://www.gurock.com/testrail/docs/api)


Install
----
Install using pip with

```bash
pip install testrail-api
```

##### Support environment variables

```dotenv
TESTRAIL_URL=https://example.testrail.com/
TESTRAIL_EMAIL=example@mail.com
TESTRAIL_PASSWORD=password
```

Example
----

```python
from datetime import datetime

from testrail_api import TestRailAPI

api = TestRailAPI("https://example.testrail.com/", "example@mail.com", "password")

# if use environment variables
# api = TestRailAPI()


new_milestone = api.milestones.add_milestone(
    project_id=1,
    name="New milestone",
    start_on=datetime.now()
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
attach = "screenshots/attach.jpg"
api.attachments.add_attachment_to_result(result["id"], attach)

api.runs.close_run(my_test_run["id"])
api.milestones.update_milestone(new_milestone["id"], is_completed=True)
```

#### Custom response handler

```python
from datetime import datetime
import simplejson

from testrail_api import TestRailAPI


def my_handler(response):
    if response.ok:
        return simplejson.loads(response.text)
    return 'Error'


api = TestRailAPI("https://example.testrail.com/", "example@mail.com", "password", response_handler=my_handler)
new_milestone = api.milestones.add_milestone(
    project_id=1,
    name="New milestone",
    start_on=datetime.now()
)

```

Contributing
----
Contributions are very welcome.

###### Getting started

* python 3.11
* pipenv 2022.12.19+

1. Clone the repository
    ```bash
    git clone https://github.com/tolstislon/testrail-api.git
    cd testrail-api
   ```
2. Install dev dependencies
    ```bash
    pipenv install --dev
    pipenv shell
   ```
3. Run the black
    ```bash
    pipenv run black
   ```
4. Run the flake8
    ```bash
    pipenv run flake8
   ```
5. Run the tests
    ```bash
    pipenv run tests
   ```
