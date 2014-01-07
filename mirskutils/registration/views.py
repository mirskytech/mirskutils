from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import authenticate, login as auth_login

from .models import Individual

from .forms import SignupForm

class Signup(View):
    
    def get(self, request):
        
        return render(request, 'registration/signup.html', {'signup_form':SignupForm()})
    
    def post(self, request):
        
        form = SignupForm(request.POST)
        
        if form.is_valid():
        
            u = User.objects.create_user(form.cleaned_data['email'],
                                         email=form.cleaned_data['email'],
                                         password=form.cleaned_data['new_password'])
            u.save()
            
            u = authenticate(username=u.username, password=form.cleaned_data['new_password'])
            auth_login(request, u)        
        
            return redirect('home')
        
        return render(request, 'registration/signup.html', {'signup_form':form})