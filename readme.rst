=================
testrail-api
=================

This is a Python wrapper of the TestRail API(v2) according to
`the official document <http://docs.gurock.com/testrail-api2/start>`_

-----------------
Install
-----------------

::

    pip install testrail-api


-----------------
Example
-----------------
::

    from testrail_api import TestRailAPI

    api = TestRailAPI('https://example.testrail.com/', 'example@mail.com', 'password')
    my_case = api.cases.get_case(22)
    api.cases.add_case(1, 'New Case', milestone_id=1)

