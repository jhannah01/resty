'''Resty API response basic handlers

These handlers provide basic constructs to build upon for creating
custom response handlers.

'''

import requests
from resty.errors import RestyError


class RestyBaseHandler(object):
    _values = {'http_response': None, 'expect_key': None}

    def parse_response(self, data, http_response=None):
        self._values['http_response'] = http_response

        if not data:
            _err_msg = 'No data in response'
            if self.http_response:
                _err_msg = '%s [HTTP Code: %s - %s]' % (_err_msg, self.http_response.status_code,
                                                        self.http_response.reason)
            raise RestyError(_err_msg, http_response=self.http_response)

        return self._handle_response(data)

    def _handle_response(self):
        raise NotImplemented('Resty handlers must implement the _handle_response method')

    @property
    def http_response(self):
        return self._values['http_response']


__all__ = ['RestyBaseHandler']
