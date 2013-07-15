from django.conf.urls import patterns, include, url

import registration.views

urlpatterns = patterns('',
                       url(r'^', registration.views.register, name="register"),
                       )