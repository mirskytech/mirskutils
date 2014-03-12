from django import forms
from django.contrib.auth import forms as auth_forms

from mirskutils.registration.forms import EmailPasswordMixin, ConfirmPasswordMixin
from .models import Individual

class SignupForm(EmailPasswordMixin, ConfirmPasswordMixin):
    pass
    
class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Individual
        fields = ('first_name', 'last_name', 'email')