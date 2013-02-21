from setuptools import setup, find_packages

setup(name='picarus',
      version='0.2.0',
      author='Brandyn A. White',
      author_email='bwhite@dappervision.com',
      license='Apache 2.0',
      package_data={'picarus.vision.data': ['*.xml', '*.pkl', '*.html', '*.jpg'],
                    'picarus.report.data': ['*.html']},
      packages=find_packages())
