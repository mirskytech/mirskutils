from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy

from .views import *
from .resources import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^foo/', include('app.foo.urls')),
    # url(r'^app/home/?$', TemplateView.as_view(template_name='app-home.html'), name="app-home"),
    # url(r'^app/redirect/?$', RedirectView.as_view(url=reverse_lazy('url-name'))),
    
)
