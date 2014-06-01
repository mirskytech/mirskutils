import os
import sys

try:
    from gevent import monkey
    monkey.patch_all()
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()    
except ImportError:
    print "WARNING: gevent module not available"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

try: 
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()
except ImportError:
    print "WARNING: could not make postgres thread safe"


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


try: 
    import uwsgi
    from uwsgidecorators import timer
    from django.utils import autoreload

    @timer(3)
    def change_code_graceful_reload(sig):
        if autoreload.code_changed():
            uwsgi.reload()
except ImportError:
    print "WARNING: auto reload disabled"


