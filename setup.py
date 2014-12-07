#!/usr/bin/env python

import os
import os
from setuptools import setup, find_packages

py_version = sys.version_info[:2]

if py_version < (2, 6):
    raise RuntimeError('On Python 2, dockerfly requires Python 2.6 or later')
elif (3, 0) < py_version < (3, 2):
    raise RuntimeError('On Python 3, dockerfly requires Python 3.2 or later')

requires = ['meld3 >= 1.0.0']
tests_require = []
if py_version < (3, 3):
    tests_require.append('mock')

testing_extras = tests_require + [
    'nose',
    'coverage',
    ]

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst')).read()
except:
    README = """\
dockerfly is a small Docker tool to help you to
create container with independent macvlan Eths easily."""

try:
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except:
    CHANGES = ''

dockerfly_version = open(os.path.join(here, 'dockerfly/version.txt')).read().strip()

setup(
    name = 'dockerfly',
    version = dockerfly_version,
    keywords = ('docker', 'dockerfly'),
    description = 'a docker tool for create containers easily',
    long_description = README + '\n\n' +  CHANGES,
    license='BSD-derived (http://www.repoze.org/LICENSE.txt)',

    url = 'https://github.com/memoryboxes/dockerfly',
    author = 'memoryboxes',
    author_email = 'memoryboxes@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires=requires,
)
