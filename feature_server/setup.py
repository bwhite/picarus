#!/usr/bin/env python
from distutils.core import setup

setup(name='feature_server',
      version='0.0.1',
      packages=['feature_server'],
      author='Andrew Miller',
      author_email='amiller@dappervision.com',
      license='GPL',
      package_data={'feature_server':['static/*/*','*.html']}
      )
