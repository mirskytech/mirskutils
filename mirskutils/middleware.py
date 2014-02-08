import datetime

from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext as _



SESSION_IDLE_TIMEOUT = getattr(settings, 'SESSION_IDLE_TIMEOUT', 1800)


class SessionIdleTimeout:
    """Middleware class to timeout a session after a specified time period.
    """
    def process_request(self, request):
        # Timeout is done only for authenticated logged in users.
        if request.user.is_authenticated():
            current_datetime = datetime.datetime.now()

            # Timeout if idle time period is exceeded.
            if request.session.has_key('last_activity') and \
                (current_datetime - request.session['last_activity']).seconds > SESSION_IDLE_TIMEOUT:
                logout(request)
                messages.add_message(request, messages.ERROR, _('Your session has been timed out.'))
            else:
                request.session['last_activity'] = current_datetime
        return None