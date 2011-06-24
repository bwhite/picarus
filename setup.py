from distutils.core import setup

setup(name='picarus',
      version='.01',
      author='Brandyn A. White',
      author_email='bwhite@dappervision.com',
      license='GPL',
      package_data={'picarus._data': ['*.xml', '*.pkl', '*.html', '*.jpg']},
      packages=['picarus', 'picarus._vision', 'picarus._cluster', 'picarus._classify', 'picarus._report', 'picarus._data'])
