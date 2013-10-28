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
    'django-tastypie',

    #'django-oauth-toolkit',
    #'django-cors-headers',
    #'django-oauth2-provider',
    
    #'psycopg2',
    'requests',
    'django-sekizai',
    'sphinxcontrib-fancybox',
    'couchdb',
    'cython', 
    #'uwsgi',
    'beautifulsoup4',
    'gevent',
    
    
    
    
]

links = [
    'https://github.com/ajmirsky/couchdb-python/tarball/master#egg=couchdb',
    'https://github.com/surfly/gevent/tarball/1.0rc3#egg=gevent',
    
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



