from setuptools import setup, find_packages

package = 'memowrth'
version = '0.1'

setup(name=package,
      version=version,
      description="",
      packages=find_packages(),
      include_package_date=True,
      url='',
      install_requires=[
          'Click',
          'beautifulsoup4',
          'requests'
      ],
      entry_points='''
      [console_scripts]
      entry_point=__main__:memworth
      ''',
      )
