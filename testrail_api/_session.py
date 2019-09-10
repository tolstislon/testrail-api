from pathlib import Path

import requests

from ._enums import METHODS


class Session:
    _user_agent = 'Python TestRail API v: 1.2'

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
        self.__session.headers['Content-Type'] = 'application/json'
        self.__session.headers.update(kwargs.get('headers', {}))
        self.__session.verify = kwargs.get('verify', True)
        self.__session.auth = (user, password)

    def request(self, method: METHODS, src: str, **kwargs):
        """Base request method"""
        url = f'{self.__base_url}{src}'
        response = self.__session.request(method=method.value, url=url, timeout=self.__timeout, **kwargs)
        if 'json' in response.headers.get('Content-Type', ''):
            return response.json()
        else:
            return response.text or None

    def attachment_request(self, method: METHODS, src: str, file: Path, **kwargs):
        """"""
        return self.request(method, src, files={'file': file.open('rb')},
                            headers={'Content-Type': 'multipart/form-data'}, **kwargs)
