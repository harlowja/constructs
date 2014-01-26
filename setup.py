#!/usr/bin/env python

# -*- coding: utf-8 -*-

# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Copyright (C) 2014 Yahoo! Inc. All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from setuptools import find_packages
from setuptools import setup


setup(name='constructs',
      version='0.0.1',
      description='Primitive structures and constructs',
      author="Joshua Harlow",
      author_email='harlowja@yahoo-inc.com',
      url='http://github.com/harlowja/constructs/',
      license="ASL 2.0",
      install_requires=[
          'six',
      ],
      packages=find_packages(),
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
      ],
      keywords="types constructs primitives",
      long_description=open("README.md", 'rb').read(),
     )
