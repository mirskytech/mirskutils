from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse

from django.core.exceptions import PermissionDenied


from decorators import method_decorator


class LoginRequiredView(View):

    permissions = []
    redirect_401 = settings.LOGIN_URL
    redirect_403 = reverse_lazy('forbidden403')
    check_active = True
    redirect_active = settings.LOGIN_URL # not used when check_active is false
        
    def dispatch(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated():
            return redirect(self.redirect_401)
        
        if not request.user.is_active and self.check_active:
            return redirect(self.redirect_active)
    
        if self.permissions and not request.user.has_perms(self.permissions):
            return redirect(self.redirect_403)
        
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)


class SessionHeartbeat(View):
    
    def get(self, request):
        return HttpResponse('heartbeat')