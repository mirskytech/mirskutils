from django.conf import settings
from django.contrib.sites.models import Site, RequestSite
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.template import Context, Template

register = template.Library()

@register.simple_tag
def urlOptions(viewname, *args, **kwargs):
    params = [ a for a in args if a ]
    kwparams = { k:v for k,v in kwargs.iteritems() if v }
    return reverse(viewname, args=params, kwargs=kwparams)

@register.filter(takes_content=True)
@stringfilter
def makeAbsolute(context, value):
    """
    takes a url and adds the site's domain name to make it an absolute URL
    """
    # TODO: should check if the url is already absolute before appending
    
    items = {
        'protocol': "https://" if context.request.is_secure() else "http://",
        'domain':RequestSite(request).domain,
        'uri':value
    }
    
    return "%(protocol)s://%(domain)s%(uri)s" % items

@register.simple_tag
def urlAbsolute(viewname, *args, **kwargs):
    return makeAbsolute(urlOptions(viewname, *args, **kwargs))