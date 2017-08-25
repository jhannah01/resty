'''Resty REST API Python module

See:
https://github.com/jhannah01/resty
'''

import os.path
import codecs
import pkg_resources
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = None

pkg_name = 'resty'
pkg_description = 'Provides a well structured result parsing and error handling for REST API clients'
pkg_requirements = [
    'beautifultable',
    'beautifulsoup4',
    'requests',
    'imaplib2',
    'simplejson',
    'sqlitedict']
pkg_keywords = 'rest api client requests',
pkg_version = '1.0.1'
pkg_license = 'GNU'

setup(
    name=pkg_name,
    version=pkg_version,
    description=pkg_description,
    long_description=long_description,
    url='https://github.com/jhannah01/%s' % pkg_name,
    license=pkg_license,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=pkg_keywords,
    packages=find_packages(exclude=['contrib', 'docs', 'tests', '.local']),
    install_requires=pkg_requirements,
)
