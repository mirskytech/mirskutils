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

    # moved below
    #'psycopg2',
    #'mysqldb',

    'python-social-auth',
    'requests',
    'django-sekizai',
    'sphinxcontrib-fancybox',
    'couchdb >= 0.9.1beta',
    'cython',

    'lxml',
    'beautifulsoup4',
    'beautifulsoup',
    
    # moved below
    #'gevent >= 1.0dev',
    #'uwsgi',
]



if os.environ.get('WITH_GEVENT',None) == 'true':
    os.environ['SERVER_INSTALL'] = 'true'
    dependencies.append('gevent >= 1.0dev')

if os.environ.get('SERVER_INSTALL', '') == 'true':
    dependencies.append('uwsgi')

if os.environ.get('WITH_MYSQL',None) == 'true':
    dependencies.append('mysqldb')
else:
    dependencies.append('psycopg2')




links = [
    'https://github.com/ajmirsky/couchdb-python/tarball/master#egg=couchdb-0.9.1beta',
    'https://github.com/surfly/gevent/tarball/1.0rc3#egg=gevent-1.0dev',
]

# force lxml to download and compile libxml and libxslt
# ( primarily for Mac OS X)
os.environ['STATICBUILD'] = 'true'

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



