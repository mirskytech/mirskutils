import json
import time

try:
    import boto
except ImportError:
    pass

from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template import RequestContext, Template
from django.http import HttpResponse, HttpResponseForbidden

from django.utils.safestring import mark_safe

#----------------------------------------------------------------------
def json_render(request, template_or_data, template_data={}, json_data={}, httpresponse = HttpResponse):
    """
    Description:
        respond to ajax request with json data (dictionary, list, string, etc) as the second argument, provide either:
    
    Arugments:
        * **template_or_data** :  (either a django.templates.Template object or a string of an existing template)
    
        * **template_data** : used as context,  if first argument is a template, to render the template. used in addition to the request context
        
        * **json_data** : additional json information if template provided
        
        * **httpresponse** : a django http response class, defaults to HttpResponse (200)
        
    Usage:
        * *python*::
        
               def get(self, request):
                    return json_response(request, 'tasks/list.html', {'list':items, 'name':'My List'}, {'status':'ok'})

                    
        * *javascript*::
        
               $.post('/api/list', function(data) {
                    console.log(data);
               })
               

        >>> { 'html' : < rendered template>, 'status':'ok' }

    """    
    
    if type(template_or_data) in (type({}), type([]), type("")):
        _response = template_or_data
    elif isinstance(template_or_data, Template):
        json_data['html'] = mark_safe(template.render(RequestContext(request,template_data)))
        _response = json_data
    else:
        json_data['html'] = render_to_string(template, template_data, context_instance=RequestContext(request))        
        _response = json_data
        
    if 'callback' not in request.REQUEST:
        return httpresponse(json.dumps(template_or_data), content_type='application/json')
    callback = "%s(%s);" % (request.REQUEST.get('callback'), json.dumps(data))   
    return httpresponse(callback, 'application/javascript')        
    

#----------------------------------------------------------------------
def render_to_json_response(request, template, template_data, json_data):
    """renders given template (either object or template name) into
    a json response, with the template having the key of ``html``.
    """
    if isinstance(template, Template):
        json_data['html'] = mark_safe(template.render(RequestContext(request,template_data)))
    else:
        json_data['html'] = render_to_string(template, template_data, context_instance=RequestContext(request))        
    return json_response(json_data)

def render_to_json(request, template, template_data, json_data):
    """alias for ``template_to_json``""" 
    return template_to_json(request, template, template_data, json_data)

#----------------------------------------------------------------------
def json_response(request, data, httpresponse = HttpResponse):
    """creates http response with a json data type with the provided data"""
    return httpresponse(json.dumps(data), 'application/json')


def jsonp_response(request, data, httpresponse = HttpResponse):
    """corollary to ``json_response`` but requires the request to have a callback"""
    if 'callback' not in request.REQUEST:
        return HttpResponseForbidden('only set up for jsonp response')
    callback = "%s(%s);" % (request.REQUEST.get('callback'), json.dumps(data))   
    return httpresponse(callback, 'application/javascript')

#----------------------------------------------------------------------
def json_redirect(request, path):
    """responds with a 'typical' json redirect command"""
    j_data = { 'status':'redirect', 'url':path  }    
    return json_response(request, j_data)

#----------------------------------------------------------------------
def sign_s3_url(url, timeout=None):
    """create a signed url for amazon s3 authetication, requires that ``boto`` be installed"""
    c = boto.connect_cloudfront(settings.CLOUDFRONT_KEY, settings.CLOUDFRONT_SECRET)
    d = c.get_streaming_distribution_info(settings.CLOUDFRONT_DISTRIBUTION_ID)
    e = int(time.time()+timeout if timeout else getattr(settings, 'CLOUDFRONT_URL_TIMEOUT', 10))
    return d.create_signed_url(url, settings.CLOUDFRONT_KEY_PAIR_ID, private_key_file=settings.CLOUDFRONT_PEM)   

#----------------------------------------------------------------------
def render_to_json(request, template, template_data, json_data):
    """alias for ``template_to_json``""" 
    return render_to_json_response(request, template, template_data, json_data)

def template_to_json(request, template, template_data, json_data):
    """**deprecated** alias for ``render_to_json_response``"""
    return render_to_json_response(request, template, template_data, json_data)