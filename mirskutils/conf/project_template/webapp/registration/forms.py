from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
        
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=255)    
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_username(self):
        if User.objects.filter(email=self.cleaned_data['username']).exists():
            raise forms.ValidationError("This username is already taken.")
        return self.cleaned_data['username']
        
    def clean_email(self):
        if User.objects.filter(username=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email is already registered.")
        return self.cleaned_data['email']
        
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255)    
    password = forms.CharField(widget=forms.PasswordInput)    
    
    
