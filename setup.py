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
    'Pillow',
    'jsonfield',
    'django-retracer',
    'South',
    'Sphinx',
    'boto',
    'django-bitfield',
    'celery',
    'django-haystack',
    'django-compressor',
    'django-fsm',
    'django-retracer',
    'django-sekizai',
    'django-tastypie',
    
    'django-bootstrap-form',
    'django-admin-bootstrapped',

    #'django-oauth-toolkit',
    #'django-cors-headers',
    #'django-oauth2-provider',
    
    'psycopg2',
    #'mysqldb',

    'python-social-auth',
    'requests',
    'django-sekizai',
    'sphinxcontrib-fancybox',
    'couchdb >= 0.9.1beta',
    'cython', 
    #'uwsgi',
    'lxml',
    'beautifulsoup4',
    #'gevent >= 1.0dev',
    
    
    
    
]

links = [
    'https://github.com/ajmirsky/couchdb-python/tarball/master#egg=couchdb-0.9.1beta',
    'https://github.com/surfly/gevent/tarball/1.0rc3#egg=gevent-1.0dev',
    
]

os.environ['STATIC_DEPS'] = True

setup(name='MirskUtils',
      version=verstr,
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



