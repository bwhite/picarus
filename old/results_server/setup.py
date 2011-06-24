#!/usr/bin/env python
from distutils.core import setup

setup(name='results_server',
      version='0.0.1',
      packages=['results_server'],
      author='Andrew Miller',
      author_email='amiller@dappervision.com',
      license='GPL',
      package_data={'results_server':['static/*/*','*.html']}
      )
