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
from testrail_api import TestRailAPI

api = TestRailAPI('https://example.testrail.com/', 'example@mail.com', 'password')
my_case = api.cases.get_case(22)
api.cases.add_case(1, 'New Case', milestone_id=1)
```
