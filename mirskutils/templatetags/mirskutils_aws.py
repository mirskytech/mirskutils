import boto
import time
from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter

from ..shortcuts import sign_s3_url

register = template.Library()

@register.filter
@stringfilter
def cfSign(url):
    return sign_s3_url(url)

