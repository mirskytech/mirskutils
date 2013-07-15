from django import http
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.template.context import Context


def server_fault(request, template_name='500.html'):
    
    t = loader.get_template(template_name)
    
    d = {
        'MEDIA_URL':settings.MEDIA_URL,
        'STATIC_URL':settings.STATIC_URL        
    }
    
    return http.HttpResponseServerError(t.render(Context(d)))

def not_found(request, template_name='404.html'):
    
    t = loader.get_template(template_name)
    d = {
        'MEDIA_URL':settings.MEDIA_URL,
        'STATIC_URL':settings.STATIC_URL
    }
    return http.HttpResponseNotFound(t.render(Context(d)))

def permission_denied(request, template_name='403.html'):
    
    t = loader.get_template(template_name)
    d = {
        'MEDIA_URL':settings.MEDIA_URL,
        'STATIC_URL':settings.STATIC_URL
    }
    return http.HttpResponseNotFound(t.render(Context(d)))
