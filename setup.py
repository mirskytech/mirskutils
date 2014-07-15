#!/usr/bin/env python

import re
import os

from distutils.core import setup
from setuptools import find_packages


VERSIONFILE="mirskutils/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


dependencies = [
    'Django',
    'jsonfield',
    'South',
    'django-compressor',
    'django-sekizai',
]


# dependency links deprecated in pip 1.5 and removed in pip 1.6
links = []


setup(name='mirskutils',
      version=verstr,
      description='Mirsky Utility Functions',
      author='Andrew',
      author_email='andrew@mirsky.net',
      scripts=[],
      url='http://mirskytech.github.io/mirskutils/',
      packages=find_packages(),
      include_package_data=True,
      install_requires=dependencies,
     )



