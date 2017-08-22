'''Helper modules for the resty Python module

This class provides basic helper methods used by the resty.
'''

import re
import os
import os.path
import logging

from resty.errors import RestyError


def get_logger(name, log_level=logging.INFO, log_filename=None,
               allow_overwrite=False, output_to_console=True):
    '''Returns a :obj:`logging.Logger` object under the provided name.

    By default, the log level will be set to :obj:`logging.INFO` but any of
    the available log levels from the `logging` class are acceptable.

    Args:
        log_level (str or int, optional): The log level to set for this logger.
        log_filename (str or None, optional): If provided, log messages will be
        written to this file.
        allow_overwrite (bool, optional): Determines if the log_filename file
        should be overwritten if it exists. (Defaults to False)
        output_to_console (bool, optional): Specifies if log messages should
        also be printed out to the console (Defaults to True)

    '''

    lvl = logging.getLevelName(log_level)
    if not re.match(r'^[A-Z]+$', lvl):
        raise ValueError('Invalid log_level specified: "%s"' % log_level)

    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if isinstance(log_level, str):
        log_level = logging.getLevelName(log_level)

    logger = logging.getLogger(log_level)
    logger.setLevel(log_level)

    if log_filename:
        if os.path.exists(log_filename) and not allow_overwrite:
            raise RestyError('Specified log_filename already exists: "%s"' % log_filename)
        if not os.path.exists(os.path.dirname(log_filename)):
            raise RestyError('Cannot find path for log_filename: "%s"' % log_filename)
        log_fh = logging.FileHandler(log_filename)
        log_fh.setLevel(log_level)
        log_fh.setFormatter(fmt)
        logger.addHandler(log_fh)

    if not log_filename or output_to_console:
        log_ch = logging.StreamHandler()
        log_ch.setLevel(log_level)
        log_ch.setFormatter(fmt)
        logger.addHandler(log_ch)

    return logger


__all__ = ['get_logger']
