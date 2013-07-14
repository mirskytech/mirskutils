#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

dependencies = [
    'Django',
    'PIL',
    'jsonfield',
    'django-retracer',
    'South',
    'Sphinx',
    'boto',
    'django-admin-tools',
    'django-bitfield',
    'celery',
    'django-celery',
    'django-compressor',
    'django-fsm',
    'django-retracer',
    'django-sekizai',
    'django-social-auth',
    'jsonfield',
    'psycopg2',
    'requests',
    'django-sekizai',
    'sphinxcontrib-fancybox',
]





setup(name='MirskUtils',
      version='0.1',
      description='Mirsky Utility Functions',
      author='Andrew',
      author_email='andrew@mirsky.net',
      url='http://andrew.mirsky.com/',
      packages=find_packages(),
      include_package_data=True,
      install_requires=dependencies
     )



