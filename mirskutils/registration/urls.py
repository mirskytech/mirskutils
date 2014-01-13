from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse_lazy

from mirskutils.registration.forms import *

from mirskutils.registration.views import *

urlpatterns = patterns('',
                       url(r'^login/$',
                           'django.contrib.auth.views.login',
                           {
                               'template_name':'registration/login.html',
                               'authentication_form':EmailAuthenticationForm
                           },
                           name="login"),
                       
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {
                               'template_name':'registration/logout.html',                           
                            },
                           name="logout"),
                       
                       # 
                       # url(r'signup/$',
                            #Signup.as_view(),
                            #name="signup"),
                       
                       # password reset
                       url(r'^password/reset/$',
                           'django.contrib.auth.views.password_reset',
                           {
                               'template_name':'registration/password-reset.html',
                               'password_reset_form':PasswordResetForm,
                            },
                           name="password-reset"),
                       
                       url(r'^password/sent/$',
                           'django.contrib.auth.views.password_reset_done',
                           {'template_name':'registration/password-reset-sent.html'}),
                       
                       url(r'^password/new/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           {'template_name':'registration/password-reset-setnew.html',
                            'set_password_form':PasswordSetNewForm,
                            'extra_context':{
                                'resetform':PasswordResetForm,
                                }},
                        
                           name="password-setnew"),
                       
                       url(r'^password/complete/$',
                           'django.contrib.auth.views.password_reset_complete',
                           {'template_name':'registration/password-reset-complete.html',
                            'extra_context': {
                                'loginform':EmailAuthenticationForm,                            
                            }},
                           name="reset-complete"),                       
                       )