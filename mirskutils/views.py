from django.views.generic import View
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse_lazy
from utils.decorators import method_decorator


class LoginRequiredView(View):
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(*args, **kwargs)