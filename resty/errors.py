'''Exceptions for errors related to the resty package

The `RestyError` class provides an extended implementation of the :obj:`Exception`
object.

'''


class RestyError(Exception):
    '''Basic error from resty

    This class is an extension of the default :obj:`Exception` class
    with extended functionality specific to this module.

    '''

    _values = {'message': None, 'base_ex': None, 'http_response': None}

    def __init__(self, message, base_ex=None, http_response=None):
        '''Initializes a new `RestyError` exception.

        If provided, this class can also store an associated :obj:`Exception` as `base_ex`
        as well as an instance of the :obj:`requests.Response` object from the time of the
        error.

        Args:
            message (str): Human-friendly error message
            base_ex (:obj:`Exception`, optional): The base :obj:`Exception`, if any
            http_response (:obj:`requests.Response`, optional) The :obj:`requests.Response`
            object, if any

        '''
        super(RestyError, self).__init__(message)
        self._values.update({'message': message, 'base_ex': base_ex, 'http_response': http_response})

    def __str__(self):
        res = self.message
        if self.base_ex:
            res = '%s (Base Error: %s)' % (res, str(self.base_ex))

        if self.http_response:
            res = '%s [HTTP Code %s - %s]' % (res, self.http_response.status_code,
                                              self.http_response.reason)

        return res

    def __repr__(self):
        res = '<RestyError(message="%s"' % self.message
        if self.base_ex:
            res = '%s, base_ex="%s"' % (res, str(self.base_ex))
        if self.http_response:
            res = '%s, http_response="Code #%s - %s"' % (res, self.http_response.status_code,
                                                         self.http_response.reason)
        res = '%s)>' % res
        return res

    @property
    def message(self):
        '''Human-friendly error message'''
        return self._values.get('message', 'Unknown Error')

    @property
    def base_ex(self):
        '''Base :obj:`Exception` associated with this error (if any)'''
        return self._values.get('base_ex', None)

    @property
    def http_response(self):
        '''The :obj:`requests.Response` object associated with this error (if any)'''
        return self._values.get('http_response', None)


__all__ = ['RestyError']
