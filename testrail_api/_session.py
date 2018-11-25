import requests


class Session:
    __default_headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'TestRail API version: {__version__}'
    }

    def __init__(self, base_url: str, user: str, password: str, **kwargs):
        self.__base_url = f'{base_url}/index.php?/api/v2/'
        self.__user = user
        self.__password = password
        self.__headers = kwargs.get('headers', {'Content-Type': 'application/json'})
        self.__timeout = kwargs.get('timeout', 10.0)
        self.__session = requests.Session()

    def printer(self):
        print(self.__default_headers)

    def request(self, method: str, src: str, **kwargs):
        """
        Base request method
        :param method:
        :param src:
        :param kwargs:
        :return: response
        """
        url = f'{self.__base_url}{src}'
        response = self.__session.request(method, url, auth=(self.__user, self.__password), headers=self.__headers,
                                          **kwargs)
        return response.json()
