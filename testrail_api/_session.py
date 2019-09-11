import logging
from pathlib import Path

import requests

from ._enums import METHODS

log = logging.getLogger(__name__)


class Session:
    _user_agent = 'Python TestRail API v: 1.3'

    def __init__(self, base_url: str, user: str, password: str, **kwargs):
        """
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
        log.info(
            'Create Session{url: %s, user: %s, password: ***, timeout: %s, headers: %s, verify: %s}',
            base_url, user, self.__timeout, self.__session.headers, self.__session.verify
        )
        self.__session.auth = (user, password)

    def __del__(self):
        self.__session.close()

    def request(self, method: METHODS, src: str, **kwargs):
        """Base request method"""
        url = f'{self.__base_url}{src}'
        if not src.startswith('add_attachment'):
            headers = kwargs.setdefault('headers', {})
            headers.update({'Content-Type': 'application/json'})

        response = self.__session.request(method=method.value, url=url, timeout=self.__timeout, **kwargs)

        log.debug('Response header: %s', response.headers)
        log.debug('Response body: %s', response.text)

        if 'json' in response.headers.get('Content-Type', ''):
            return response.json()
        else:
            return response.text or None

    def attachment_request(self, method: METHODS, src: str, file: Path, **kwargs):
        """"""
        with file.open('rb') as attachment:
            return self.request(method, src, files={'attachment': attachment}, **kwargs)
