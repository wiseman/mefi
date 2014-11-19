#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup


# Work around setuptools bug
# http://article.gmane.org/gmane.comp.python.peak/2509
import multiprocessing


PACKAGE_NAME = 'mefi'
VERSION = '0.0.2'


settings = dict(
  name=PACKAGE_NAME,
  version=VERSION,
  description='Metafilter utilities.',
  long_description='Code relevant to scraping and processing data from metafilter.com.',
  author='John Wiseman',
  author_email='jjwiseman@gmail.com',
  url='https://github.com/wiseman/mefi',
  packages=['mefi'],
  test_suite='nose.collector',
  install_requires=[
    'pattern',
    'BeautifulSoup'
    ],
  tests_require=[
    'nose'
    ],
  license='MIT',
  classifiers=(
    # 'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Programming Language :: Python',
    # 'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    ),
  )


setup(**settings)
