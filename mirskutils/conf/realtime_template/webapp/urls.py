from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import core.views

handler500 = core.views.server_fault
handler404 = core.views.not_found
handler403 = core.views.permission_denied

if settings.DEBUGGER:
    import wingdbstub


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'app.views.home', name='home'),
    # url(r'^foo/', include('app.foo.urls')),
    # url(r'^app/home/?$', TemplateView.as_view(template_name='app-home.html'), name="app-home"),
    # url(r'^app/redirect/?$', RedirectView.as_view(url=reverse_lazy('url-name'))),
    
         

    url(r'^', include('webapp.registration.urls')),
    url(r'^', include('django.contrib.auth.urls')), 
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^heartbeat/$', 'mirskutils.views.SessionHeartbeat'),
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
