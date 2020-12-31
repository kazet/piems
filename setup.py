#!/usr/bin/env python

from distutils.core import setup

setup(name='piems',
      version='1.0',
      description='piems - command-line time interval calculator',
      author='Krzysztof Zając',
      author_email='krzysztof.zajac2@gmail.com',
      url='https://github.com/kazet/piems',
      packages=['piems'],
      scripts=['piems/scripts/piems'],
)
