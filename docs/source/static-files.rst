.. _static-file-management:

static file management
==============================================

environment configuration
-------------------------------------

By convention, the django project template included in this package uses::

    STATIC_ROOT = os.path.join(PROJECT_PATH, "site_static")
    STATIC_URL = "/static/"

During development (ie `DEBUG=True`), the django.static.staticfiles handler
will find all your various static files. In production, run `./manage.py collectatic`
to gather all the static files.


import statements
-------------------------------------

This setup will also allow you to have import statements, but the paths need to be relative to `static`.

for example, if your static file is in `myapp/static/myapp/mylessfile.less`, the import statement would be::

    @import "/static/script/textarea.css";


css (and less,sass) and javascript
----------------------------------------------

The project template is setup with sekizai tags (a convenient way of 
specifiy your scripts in any page but all of them rendering in one place) and 
compress (preprocessor of files as well as concatenation & minimization). To enable 
the precompilers, uncomment this line towards the bottom of the `settings.py` file::


    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )