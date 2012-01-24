from setuptools import setup, find_packages

setup(name='picarus',
      version='.01',
      author='Brandyn A. White',
      author_email='bwhite@dappervision.com',
      license='GPL',
      package_data={'picarus.vision.data': ['*.xml', '*.pkl', '*.html', '*.jpg'],
                    'picarus.report.data': ['*.html']},
      packages=find_packages())
#['picarus', 'picarus.vision', 'picarus.vision.data', 'picarus.cluster', 'picarus.classify',
#'picarus.report', 'picarus.report.data', 'picarus.io']
