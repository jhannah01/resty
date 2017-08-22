'''REST API Client class

Provides the actual class to interact with REST API interfaces

'''

import requests
from urllib import urlencode
from urlparse import urlparse, urljoin
from contextlib import closing

from resty.errors import RestyError
from resty.handlers import RestyBaseHandler


class RestyClient(object):
    '''Resty API client interface

    This class provides the actual functionality to interact with REST
    API interfaces as well as structured result parsing and sane error
    handling.

    '''

    _values = {'base_uri': None, 'auth_headers': {}, 'response_handler': None}
    _http_verbs = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    def __init__(self, base_uri, auth_headers=None, response_handler=None):
        self.base_uri = base_uri

        if auth_headers:
            self.auth_headers = auth_headers

        if response_handler and not isinstance(response_handler, RestyBaseHandler):
            raise ValueError('Invalid response_handler specified. Must be a subclass of RestyBaseHandler.')

        self._values['response_handler'] = response_handler

    def call(self, path, http_verb='GET', qs_params=None, req_params=None, ext_headers=None, as_json=True,
             skip_response_handler=False):
        u = urljoin(self.base_uri, path)

        http_verb = http_verb.upper()

        if http_verb not in self._http_verbs:
            valid_verbs = '", "'.join(self._http_verbs)
            raise ValueError('Invalid HTTP verb specified: "%s". Must be one of: "%s"' % (http_verb, valid_verbs))

        if qs_params:
            u = '%s?%s' % urlencode(qs_params)

        if not ext_headers:
            ext_headers = {}

        if self.auth_headers:
            ext_headers.update(self.auth_headers)

        resp = None
        results = None
        try:
            with closing(requests.request(http_verb, u, params=req_params,
                                          headers=ext_headers)) as resp:
                if not resp.status_code != '200':
                    raise RestyError('Invalid API response: "%s"' % resp.content,
                                     http_response=resp)

                if as_json:
                    try:
                        results = resp.json()
                    except ValueError:
                        raise RestyError('Non-JSON response from API: "%s"' % resp.content,
                                         http_response=resp)
                else:
                    results = resp.content
        except requests.exceptions.RequestException as ex:
            raise RestyError('Error communicating with REST API: %s' % str(ex), base_ex=ex,
                             http_response=resp)

        if not self.response_handler or skip_response_handler:
            return results

        return self.response_handler.parse_response(results, http_response=resp)

    @property
    def base_uri(self):
        '''The base URI (including path, if required) of the API to be called

        The URI should be the base URI that will be used for making all API requests.
        It should only contain the HTTP scheme, hostname, path and (optionally) the
        port used to make the API requests.

        Examples:
            For most cases the URI will be fairly straight-forward.

            >>> my_uri = 'https://api.testing.com/api/path'
            >>> resty_client = RestyClient(my_uri)

            If the API is running on a non-standard port (i.e. 8080) you
            may specify this in the URI string as well.

            >>> my_uri = 'http://altapi.testing.com:8080/api/path'
            >>> resty_client = RestyClient(my_uri)

        '''

        return self._values.get('base_uri', None)

    @base_uri.setter
    def base_uri(self, value):
        uri = urlparse(value)

        if (uri.scheme not in ['http', 'https']) or (not uri.hostname):
            raise ValueError('Invalid URI: "%s"' % value)

        if not value.endswith('/'):
            value = '%s/' % value

        self._values['base_uri'] = value

    @property
    def auth_headers(self):
        '''Optional authorization headers to be passed when making API requests

        This value should be a dictionary containing the name, value pairs for
        authorizing API requests made.

        Examples:
            If you needed to pass an 'Authorization' header with the value of
            '123456789abcdef' as your key it would look something like this.

            >>> resty_client = RestyClient(my_uri, auth_headers={'Authorization': '123456789abcdef'})

            You may also later update the authorization headers by setting the
            new value (or None) to the property `auth_headers`.

            >>> resty_client.auth_headers = {'Authorization': 'ABCDEF987654321'}

        '''
        return self._values.get('auth_headers', {})

    @auth_headers.setter
    def auth_headers(self, value):
        if not value:
            self._values['auth_headers'] = {}
            return

        if not isinstance(value, dict):
            raise TypeError('Invalid type for auth_headers: must be a dict')

        self._values['auth_headers'] = value

    @property
    def response_handler(self):
        return self._values['response_handler']


__all__ = ['RestyClient']
