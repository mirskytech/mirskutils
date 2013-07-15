from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.template.context import RequestContext

from forms import RegistrationForm



def register(request):
    
    form = RegistrationForm()
    
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(form.cleaned_data['username'],
                                     email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'])
            
            return redirect('home')
        
            
            
    
    
    d = {
    'form':form
    
    }
    
    return render_to_response('registration/registration_form.html', d, context_instance = RequestContext(request))