# -*- coding: utf-8 -*-
import os
gettext = lambda s: s

DEBUG = True
TEMPLATE_DEBUG = True
DEBUGGER = True

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(PROJECT_PATH, "site_static")
STATIC_URL = "/static/"

ADMIN_MEDIA_PREFIX="/static/admin/"

SESSION_COOKIE_DOMAIN = 'starter-app.com'

# to compress js/css 'static' files using sekizai & compressor
COMPRESS_OUTPUT_DIR = "CACHE"
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

#WINGHOME_PATH="/usr/lib/wingide4.1"
WINGHOME = '/Applications/WingIDE.app/Contents/MacOS/'


ACCOUNT_ACTIVATION_DAYS = 7


## EMAIL SETTINGS
ADMINS = (
    ('Super User', 'admin@domain.com'),
)

MANAGERS = ADMINS

SERVER_EMAIL = ''
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST='localhost'
EMAIL_PORT='1025'


############## COMMON APP SETTINGS


# for django-social-auth
#FACEBOOK_APP_ID = ''
#FACEBOOK_API_SECRET = ''

#for couchdb
#COUCHDB_SERVER = 'http://localhost:5984'
#COUCHDB_USERNAME = ''
#COUCHDB_PASSWORD = ''

# for celeryd
#BROKER_URL = 'amqp://user:password@localhost:5672/queuename'   # for rabbitmq
#BROKER_URL = 'couchdb://user:password@localhost:5984/queuename' # for couchdb

# for boto
#AWS_ACCESS_KEY_ID = ''
#AWS_SECRET_ACCESS_KEY = ''
#CLOUDFRONT_EXPIRES_IN = 60*60
#CLOUDFRONT_KEY_PAIR_ID = ''
#CLOUDFRONT_KEY = ''
#CLOUDFRONT_SECRET = ''

# for haystack/solr search
#HAYSTACK_CONNECTIONS = {
    #'default': {
        #'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        #'URL': 'http://127.0.0.1:8983/solr'
        ## ...or for multicore...
        ## 'URL': 'http://127.0.0.1:8983/solr/mysite',
    #},
#}