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
    'django-bitfield',
    'celery',
    'django-celery',
    'django-compressor',
    'django-fsm',
    'django-retracer',
    'django-sekizai',
    'django-tastypie',

    'psycopg2',
    #'mysqldb',

    'python-social-auth',
    'django-bootstrap-form',
    'django-admin-bootstrapped',
    'requests',
    'django-sekizai',
    'sphinxcontrib-fancybox',
    'couchdb >= 0.9.1beta',
    'cython', 
    #'uwsgi',
    'beautifulsoup4',
    'gevent >= 1.0dev',
    
    
    
    
]

links = [
    'https://github.com/ajmirsky/couchdb-python/tarball/master#egg=couchdb-0.9.1beta',
    'https://github.com/surfly/gevent/tarball/1.0rc3#egg=gevent-1.0dev',
    
]

setup(name='MirskUtils',
      version='0.1',
      description='Mirsky Utility Functions',
      author='Andrew',
      author_email='andrew@mirsky.net',
      scripts=['bin/mirskutils-admin.py'],
      url='http://andrew.mirsky.com/',
      packages=find_packages(),
      include_package_data=True,
      install_requires=dependencies,
      dependency_links = links,
     )



