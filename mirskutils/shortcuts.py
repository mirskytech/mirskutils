import json

from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.template import RequestContext, Template
from django.http import HttpResponse, HttpResponseForbidden

from django.utils.safestring import mark_safe

def template_to_json(request, template, template_data, json_data):
    if isinstance(template, Template):
        json_data['html'] = mark_safe(template.render(RequestContext(request,template_data)))
    else:
        json_data['html'] = render_to_string(template, template_data, context_instance=RequestContext(request))        
    return HttpResponse(json.dumps(json_data), content_type='application/json')

def render_to_json(request, template, template_data, json_data):    
    return template_to_json(request, template, template_data, json_data)

def json_response(request, data):
    return HttpResponse(json.dumps(data), content_type='application/json')

def jsonp_response(request, data):
    if 'callback' not in request.REQUEST:
        return HttpResponseForbidden('only set up for jsonp response')
    callback = "%s(%s);" % (request.REQUEST.get('callback'), json.dumps(data))   
    return HttpResponse(callback, 'application/javascript')

def json_redirect(request, path):
    j_data = { 'status':'redirect', 'url':path  }    
    return json_response(request, j_data)