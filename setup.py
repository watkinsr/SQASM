#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
from setuptools import setup, find_packages
from codecs import open

AUTHOR = 'Ryan Watkins'
AUTHOR_GH = 'watkinsr'
AUTHOR_MAIL = 'ryanwatkins54@gmail.com'
PACKAGE_NAME = 'sqasm'
LICENSE = 'MIT'
DESCRIPTION = 'SQASM is an interpreted register based, simulated, quantum programming language'
KEYWORDS = 'quantum programming language simulator'
REQUIRED_PACKAGES = [
    'requests',
]
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU v3',
    'Programming Language :: Python :: 2.7',
]

######################################################################

_here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read().strip()

with open(os.path.join(_here, 'VERSION.txt'), 'r') as f:
    VERSION = f.read().strip()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    download_url='https://github.com/{}/{}/tarball/v{}'.format(AUTHOR_GH, PACKAGE_NAME, VERSION),
    long_description=LONG_DESCRIPTION,
    url='https://github.com/{}/{}'.format(AUTHOR_GH, PACKAGE_NAME),
    author=AUTHOR,
    author_email=AUTHOR_MAIL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    # packages=find_packages(),
    py_modules=['sqasm'],
    install_requires=REQUIRED_PACKAGES,
)
