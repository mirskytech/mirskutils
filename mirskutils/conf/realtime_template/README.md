




To run a non-blocking app, use::

    uwsgi --gevent 100 --http :3031 --master --module wsgi


References
=====================

* http://uwsgi-docs.readthedocs.org/en/latest/Gevent.html
* http://uwsgi-docs.readthedocs.org/en/latest/Async.html
* http://codysoyland.com/2011/feb/6/evented-django-part-one-socketio-and-gevent/