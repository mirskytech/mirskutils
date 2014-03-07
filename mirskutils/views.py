
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages

from django.core.exceptions import PermissionDenied
from decorators import method_decorator



class LoginRequiredView(View):
    """Subclass of django.views.generic.View which handles authentication
    replaces the use of @method_decorator in urls.py (for class-based views) or 
    views.py (for function-based views)

    Options:
       * **permissions** : additional permissions to check
       * **redirect_401** : redirect location for non-authenticated user
       * **redirect_403** : redirect location for a forbidden operation
       * **check_active** : include ``is_active`` in the check for authentication
       * **redirect_active** : redirect location if a user is inactive (n/a when ``check_active = False``)

    """     

    permissions = []
    redirect_401 = settings.LOGIN_URL
    redirect_403 = reverse_lazy('forbidden403')
    check_active = True
    redirect_active = settings.LOGIN_URL # not used when check_active is false
    login_required_message = "Login Required."
        
    def dispatch(self, request, *args, **kwargs):
        """
        overrides the default display method in order to check authentication
        """
        
        # TODO : include ?next=
        if not request.user.is_authenticated():
            if self.login_required_message:
                messages.info(request, self.login_required_message)
            return redirect(self.redirect_401)
        
        if not request.user.is_active and self.check_active:
            return redirect(self.redirect_active)
    
        if self.permissions and not request.user.has_perms(self.permissions):
            return redirect(self.redirect_403)
        
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


class SessionHeartbeat(View):
    """Receives a periodic request to keep a users session active
    
    For use with :func:`middleware.SessionTimeout` and ``{{ STATIC_URL }}js/heartbeat.js``
    """    
    def get(self, request):
        return HttpResponse('heartbeat')