#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup

#with open('requirements.txt') as f:
    #requirements = f.read().splitlines()

setup(name='natural-disasters',
      version='0.0.1',
      description='Reports on natural disaster data extracted from the EONET API from NASA',
      author='Keith Lee',
      author_email='code@keithlee.co.uk',
      url='https://github.com/keithlee-co-uk/natural-disasters',
      packages=['natural-disasters'],
      dependency_links = ['git+git://github.com/keithlee-co-uk/defaultargs#egg=defaultargs',
      'git+git://github.com/keithlee-co-uk/dbconnection.git#egg=dbconnection'],
      install_requires=["requests",
                        "dbconnection",
                        "defaultargs"],
      #install_requires=[requirements],

      )
