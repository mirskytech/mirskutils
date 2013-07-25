import boto
import time
from django.conf import settings

from mirskutils.shortcuts import sign_s3_url


@register.filter
@stringfilter
def cfSign(url):
    return sign_s3_url(url)

