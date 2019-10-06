import logging
import os
import time
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Union, Optional

import requests

from .__version__ import __version__
from ._enums import METHODS
from ._exception import StatusCodeError, TestRailError

log = logging.getLogger(__name__)


class Session:
    _user_agent = f'Python TestRail API v: {__version__}'

    def __init__(self,
                 url: Optional[str] = None,
                 email: Optional[str] = None,
                 password: Optional[str] = None,
                 exc: bool = False,
                 rate_limit: bool = True,
                 **kwargs):
        """
        :param url: TestRail address
        :param email: Email for the account on the TestRail
        :param password: Password for the account on the TestRail
        :param exc: Catching exceptions
        :param kwargs:
            :key timeout int
            :key verify bool
            :key headers dict
        """
        _url = url or os.environ.get('TESTRAIL_URL')
        _email = email or os.environ.get('TESTRAIL_EMAIL')
        _password = password or os.environ.get('TESTRAIL_PASSWORD')
        if not _url or not _email or not _password:
            raise TestRailError('No url or email or password values set')
        if _url.endswith('/'):
            _url = _url[:-1]
        self.__base_url = f'{_url}/index.php?/api/v2/'
        self.__timeout = kwargs.get('timeout', 30)
        self.__session = requests.Session()
        self.__session.headers['User-Agent'] = self._user_agent
        self.__session.headers.update(kwargs.get('headers', {}))
        self.__session.verify = kwargs.get('verify', True)
        self.__user_email = _email
        self.__session.auth = (self.__user_email, _password)
        self.__exc = exc
        self._rate_limit = rate_limit
        log.info(
            'Create Session{url: %s, user: %s, timeout: %s, headers: %s, verify: %s, exception: %s}',
            url, self.__user_email, self.__timeout, self.__session.headers, self.__session.verify, self.__exc
        )

    @property
    def user_email(self) -> str:
        return self.__user_email

    def __response(self, response: requests.Response):
        if not response.ok:
            log.error('Code: %s, reason: %s url: %s, content: %s',
                      response.status_code, response.reason, response.url, response.content)
            if not self.__exc:
                raise StatusCodeError(response.status_code, response.reason, response.url, response.content)

        log.debug('Response body: %s', response.text)
        try:
            return response.json()
        except (JSONDecodeError, ValueError):
            return response.text or None

    def request(self, method: METHODS, src: str, raw: bool = False, **kwargs):
        """Base request method"""
        url = f'{self.__base_url}{src}'
        if not src.startswith('add_attachment'):
            headers = kwargs.setdefault('headers', {})
            headers.update({'Content-Type': 'application/json'})

        iterations = 3
        for count in range(iterations):
            try:
                response = self.__session.request(method=method.value, url=url, timeout=self.__timeout, **kwargs)
            except Exception as err:
                log.error('%s', err, exc_info=True)
                raise
            if self._rate_limit and response.status_code == 429 and count < iterations - 1:
                time.sleep(2)
                continue
            log.debug('Response header: %s', response.headers)
            return response if raw else self.__response(response)

    @staticmethod
    def _path(path: Union[Path, str]) -> Path:
        return path if isinstance(path, Path) else Path(path)

    def attachment_request(self, method: METHODS, src: str, file: Union[Path, str], **kwargs):
        """"""
        file = self._path(file)
        with file.open('rb') as attachment:
            return self.request(method, src, files={'attachment': attachment}, **kwargs)

    def get_attachment(self, method: METHODS, src: str, file: Union[Path, str], **kwargs) -> Path:
        """"""
        file = self._path(file)
        response = self.request(method, src, raw=True, **kwargs)
        if response.ok:
            with file.open('wb') as attachment:
                attachment.write(response.content)
            return file
        return self.__response(response)
