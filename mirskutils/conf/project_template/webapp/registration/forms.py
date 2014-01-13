from django import forms
from django.contrib.auth import forms as auth_forms

from mirskutils.registration.forms import EmailPasswordMixin, ConfirmPasswordMixin


class SignupForm(EmailPasswordMixin, ConfirmPasswordMixin):
    pass
    
