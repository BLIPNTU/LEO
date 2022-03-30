#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# blipleo is available on PyPI
# Normally people should install blipleo using the following pip commmand
# pip install blipleo

'''
Setup script for blipleo

Latest version can be found at https://github.com/BLIPNTU/LEO

:copyright: (c) 2021 Le Tuan Anh <tuananh.ke@gmail.com>
:license: GPL version 3.0, see LICENSE for more details.
'''

import io
from setuptools import setup


def read(*filenames, **kwargs):
    ''' Read contents of multiple files and join them together '''
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


requirements = ['pyinkscape >= 0.1a3', 'chirptext >= 0.1a20', 'PyPDF2']


readme_file = 'README.md'
long_description = read(readme_file)
pkg_info = {}
exec(read('blipleo/__version__.py'), pkg_info)


setup(
    name='blipleo',  # package file name (<package-name>-version.tar.gz)
    version=pkg_info['__version__'],
    url=pkg_info['__url__'],
    project_urls={
        "Bug Tracker": "https://github.com/BLIPNTU/LEO/issues",
        "Source Code": "https://github.com/BLIPNTU/LEO/"
    },
    keywords="nlp",
    license=pkg_info['__license__'],
    author=pkg_info['__author__'],
    tests_require=requirements,
    install_requires=requirements,
    author_email=pkg_info['__email__'],
    description=pkg_info['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['blipleo'],
    package_data={'blipleo': ['templates/*.svg']},
    include_package_data=True,
    platforms='any',
    test_suite='test',
    # Reference: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.11',
                 'Development Status :: {}'.format(pkg_info['__status__']),
                 'Natural Language :: English',
                 'Environment :: Plugins',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: {}'.format(pkg_info['__license__']),
                 'Operating System :: OS Independent',
                 'Topic :: Multimedia :: Graphics',
                 'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
