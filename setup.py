#!/usr/bin/env python

import os

from distutils.core import setup


with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requires = f.read().splitlines()


setup(name='piems',
      version='1.0',
      description='piems - command-line time interval calculator',
      author='Krzysztof Zając',
      author_email='krzysztof.zajac2@gmail.com',
      url='https://github.com/kazet/piems',
      packages=['piems'],
      scripts=['piems/scripts/piems'],
      install_requires=requires
)
