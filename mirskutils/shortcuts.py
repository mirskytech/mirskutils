import json
import boto
import time

from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template import RequestContext, Template
from django.http import HttpResponse, HttpResponseForbidden

from django.utils.safestring import mark_safe

#----------------------------------------------------------------------
def json_response(request, template_or_data, template_data={}, json_data={}):
    """
    response to ajax request with json data (dictionary, list, string, etc)
    
    :param request: django Request object
    :param data: json data to be sent with the response
    :type data: ``{}``, ``[]`` or ``""``
    :rtype: django.http.HttpResonse
    
    """
    
    if type(template_or_data) in (type({}), type([]), type("")):
        return HttpResponse(json.dumps(template_or_data), content_type='application/json')
    return template_to_json(request, template_or_data, template_data, json_data)


#----------------------------------------------------------------------    
def template_to_json(request, template, template_data, json_data):
    """respond to ajax request by rendering template

    Arguments:
        * **request** : django's request object
        * **template** : name of the template or a Template object
        * **template_data** : context, additional to the request context, used to render the template
        json_data : extra json data to be included in the response

    Return:
        django.http.HttpResponse
        
    Raises:
        n/a
    
    Usage:
       *in python* : ``
    def get(self, request):
    
        ...
        
        return template_to_json(request, 'tasks/list.html', {'list':items, 'name':'My List'}, {'status':'ok'})
    
    ``
    
        javascript : ``
    $.post('/api/list', function(data) {
       console.log(data);
    })
    
    >> { 'html' : < rendered template>, 'status':'ok' }
    ``
    """    
    if isinstance(template, Template):
        json_data['html'] = mark_safe(template.render(RequestContext(request,template_data)))
    else:
        json_data['html'] = render_to_string(template, template_data, context_instance=RequestContext(request))        
    return json_response(json_data)

def render_to_json(request, template, template_data, json_data):
    """respond to ajax request by rendering template


    Args:
    
        arg1 (str): argument one
        arg2 (bool): argument two

    Returns:
        < description of return >
        
        ``< example of return >``
        
    Raises:
        Exception: an exception that could be raised
    
    Usage:
    
    python : ``    ``
    
    javascript : ``
        $.post('/api/list', function(data) {
            console.log(data);
        });
    
    >> { 'html' : < rendered template>, 'status':'ok' }
    ``
    """ 
    return template_to_json(request, template, template_data, json_data)


def jsonp_response(request, data, httpresponse = HttpResponse):
    if 'callback' not in request.REQUEST:
        return HttpResponseForbidden('only set up for jsonp response')
    callback = "%s(%s);" % (request.REQUEST.get('callback'), json.dumps(data))   
    return httpresponse(callback, 'application/javascript')

def json_redirect(request, path):
    j_data = { 'status':'redirect', 'url':path  }    
    return json_response(request, j_data)


def sign_s3_url(url, timeout=None):
    c = boto.connect_cloudfront(settings.CLOUDFRONT_KEY, settings.CLOUDFRONT_SECRET)
    d = c.get_streaming_distribution_info(settings.CLOUDFRONT_DISTRIBUTION_ID)
    e = int(time.time()+timeout if timeout else getattr(settings, 'CLOUDFRONT_URL_TIMEOUT', 10))
    return d.create_signed_url(url, settings.CLOUDFRONT_KEY_PAIR_ID, private_key_file=settings.CLOUDFRONT_PEM)   



