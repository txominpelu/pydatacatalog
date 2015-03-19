#!/usr/bin/env python

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

import os

from setuptools import setup, find_packages


PROJECT = u'pydatacatalog'
VERSION = '0.1'
URL = ''
AUTHOR = u'Inigo Mediavilla'
AUTHOR_EMAIL = u'imediavilla@viadeoteam.com'
DESC = "A short description..."

def read_file(file_name):
    file_path = os.path.join(
        os.path.dirname(__file__),
        file_name
        )
    return open(file_path).read()

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=read_file('README.rst'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=read_file('LICENSE'),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    packages = find_packages("."),  # include all packages under src
    package_dir = {'': "."},   # tell distutils packages are under src
    install_requires=[
        # -*- Requirements -*-
        "argparse",
        "pytz",
        "requests",
        "wsgiref"
    ],
    entry_points = {
        # -*- Entry points -*-
    },
    classifiers=[
    	# see http://pypi.python.org/pypi?:action=list_classifiers
        # -*- Classifiers -*- 
        "Programming Language :: Python",
    ],
    test_suite = "pydatacatalog.test.datacatalog_test"
)
