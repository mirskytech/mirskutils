from django import forms
from django.contrib.auth import get_user_model

class EmailPasswordMixin(forms.Form):
    
    email = forms.EmailField()
    new_password = forms.CharField(
        label=_("confirm password"),
        widget=forms.PasswordInput(attrs={'placeholder':'new password'}),
        max_length=35
        )
    
    def clean_email(self):
        
        if 



class ConfirmPasswordMixin(forms.Form):
    confirm_password = forms.CharField(
        label=_("confirm password"),
        widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}),
        max_length=35
        )   
        
    def clean(self):
        cleaned_data = super(ConfirmPasswordMixin, self).clean()
        if cleaned_data.get('new_password','') != cleaned_data.get('confirm_password', ''):
            raise forms.ValidationError("the passwords don't match")
        return cleaned_data