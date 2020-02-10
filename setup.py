#!/usr/bin/env python3

import setuptools
from distutils.core import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(name="phg",
      version='0.1',
      author='Ulises Rosas',
      long_description = readme,
      long_description_content_type = 'text/markdown',
      author_email='ulisesfrosasp@gmail.com',
      packages = ['phg'],
      package_dir = {'phg': 'src'},
     # scripts = ['src/geneTable.py'],
     # entry_points={
     #   'console_scripts': [
     #      ' = phg.xxx:main'
     #       ]
     # },
      classifiers = [
             'Programming Language :: Python :: 3',
             'License :: OSI Approved :: MIT License'
             ]
    )