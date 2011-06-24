from distutils.core import setup

setup(name='picarus',
      version='.01',
      author='Brandyn A. White',
      author_email='bwhite@dappervision.com',
      license='GPL',
      package_data={'picarus': ['*.xml', '*.pkl', '*.html']},
      packages=['picarus'])
