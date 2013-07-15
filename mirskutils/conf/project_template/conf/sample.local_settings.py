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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

WINGHOME_PATH="/usr/lib/wingide4.1"


ACCOUNT_ACTIVATION_DAYS = 7


## EMAIL SETTINGS
ADMINS = (
    ('Andrew Mirsky', 'your_email@domain.com'),
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

#CLOUDFRONT_EXPIRES_IN = 60*60
#CLOUDFRONT_KEY_PAIR_ID = ''
#CLOUDFRONT_KEY = ''
#CLOUDFRONT_SECRET = ''

#FACEBOOK_APP_ID = ''
#FACEBOOK_API_SECRET = ''