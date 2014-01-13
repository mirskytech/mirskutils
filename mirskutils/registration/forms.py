from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import forms as auth_forms


class EmailPasswordMixin(forms.Form):
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder':'email address'})
    )
    
    new_password = forms.CharField(
        label=_("confirm password"),
        widget=forms.PasswordInput(attrs={'placeholder':'new password'}),
        max_length=35
        )
    
    def clean_email(self):
                
        if get_user_model().objects.filter(username=self.cleaned_data['email']):
            raise forms.ValidationError("email is already registered")

        return self.cleaned_data['email']
    
    def clean(self):
        return self.cleaned_data
    

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
    
    
class EmailAuthenticationForm(auth_forms.AuthenticationForm):
    
    username = forms.EmailField(
        max_length=254,
        label="email address",
        widget=forms.TextInput(attrs={'placeholder':'email address'})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'placeholder':'password'})
    )

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }
    
    
class PasswordResetForm(auth_forms.PasswordResetForm):
    
    email = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder':'email address'})
    )
    
    error_messages = {
        'unknown': _("That email address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': _("The user account associated with this email "
                      "address cannot reset the password."),
    }
    
    
class PasswordChangeForm(auth_forms.PasswordChangeForm):
    
    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'old password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'confirm new password'
        
class PasswordSetNewForm(auth_forms.SetPasswordForm):
    
    def __init__(self, *args, **kwargs):
        super(PasswordSetNewForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = 'new password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'confirm new password'
