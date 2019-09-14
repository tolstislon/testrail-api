import logging
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Union
from .__version__ import __version__

import requests

from ._enums import METHODS

log = logging.getLogger(__name__)


class TestRailAPIError(Exception):
    pass


class StatusCodeError(TestRailAPIError):
    pass


class Session:
    _user_agent = f'Python TestRail API v: {__version__}'

    def __init__(self, base_url: str, user_email: str, password: str, exc: bool = False, **kwargs):
        """
        :param base_url: TestRail address
        :param user_email: Email for the account on the TestRail
        :param password: Password for the account on the TestRail
        :param exc: Catching exceptions
        :param kwargs:
            :key timeout int
            :key verify bool
            :key headers dict
        """
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        self.__base_url = f'{base_url}/index.php?/api/v2/'
        self.__timeout = kwargs.get('timeout', 30)
        self.__session = requests.Session()
        self.__session.headers['User-Agent'] = self._user_agent
        self.__session.headers.update(kwargs.get('headers', {}))
        self.__session.verify = kwargs.get('verify', True)
        self.__user_email = user_email
        self.__session.auth = (self.__user_email, password)
        self.__exc = exc
        log.info(
            'Create Session{url: %s, user: %s, timeout: %s, headers: %s, verify: %s, exception: %s}',
            base_url, self.__user_email, self.__timeout, self.__session.headers, self.__session.verify, self.__exc
        )

    @property
    def user_email(self) -> str:
        return self.__user_email

    def __del__(self):
        self.__session.close()

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

        try:
            response = self.__session.request(method=method.value, url=url, timeout=self.__timeout, **kwargs)
        except Exception as err:
            log.error('%s', err, exc_info=True)
            raise

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
