

project templates
======================================

As of Django 1.5, you can install the templates included in ``mirskutils`` by specifying::

    django-admin.py startproject --template=<python env>/lib/python2.7/site-packagse/mirskutils/conf/project_template MyProjectName

Each project comes with one or more ``requirements.txt`` file depending on which packages you might need; it can 
be found under the ``conf`` subdirectory.


django project
------------------------------------

a quick way of creating a new project with the most commonly used elements::

    project/
        manage.py  # django project management
        wsgi.py    # web application entry point
        conf/      # sample configuration files for the project
        docs/      # initial sphinx documentation setup
        mobileapp/ # location (currently empty) for the project's mobile app
        webapp/    # django project struction
        
        


..standardprojectemplate

standard request-response project
++++++++++++++++++++++++++++++++++++++++++++

to use::

    >> django-admin.py startproject MyProjectName

The django portion -- under `webapp/` -- includes this structure and elements::

    webapp/
        api.py                      # location for any api instantiations
        basic_init.sample.json      # example of a fixture
        core/                       # core applications of this project
            <your app here>
        registration/               # urls, configuration and templates for django.contrib.auth
        routers.py                  # 
        settings.py
        static
        templates
        urls.py
        wingstub.py
        
api.py:
    location for any api singleton instantiations

basic_init.sample.json:
    example of a django fixture for loading data
    
core:
    location for the core applications of this project
    
routers.py:
    a utility to direct all models of a certain type to a specified database
    
settings.py:
    basic configuration
    
static:
    project-wide static files
    
templates:
    base, 404, 500 and 403 templates
    
urls.py:
    master url file with examples
    
wingstub.py:
    utility to connect to WingIDE's remote debugging
    
    
realtime project
++++++++++++++++++++++++++++++++++++++++++++

this project includes the :ref:`standardprojectemplate` plus the necessary application configuration, requirements file
and examples for django to create long-running connections with a user's browsers:

    ::
    
        >> django-admin.py startproject --template=<python env>lib/python2.7/site-packagse/mirskutils/conf/realtime_project MyProjectName
    
django + frontend mvc
++++++++++++++++++++++++++++++++++++++++++++

    ***coming soon***
    
