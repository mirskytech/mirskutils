from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from django.core.exceptions import PermissionDenied


from decorators import method_decorator


class LoginRequiredView(View):

    permissions = []
    redirect_401 = settings.LOGIN_URL
    redirect_403 = reverse_lazy('forbidden403')
        
    #@method_decorator(login_required)
    #@method_decorator(permission_required(['people.verifier_express',]))
    def dispatch(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated():
            return redirect(self.redirect_401)
    
        if self.permissions and not request.user.has_perm(*self.permissions):
            return redirect(self.redirect_403)
        
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)
