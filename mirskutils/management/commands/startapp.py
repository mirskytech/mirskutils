import os

from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.utils.importlib import import_module

import mirskutils


class Command(TemplateCommand):
    help = ("MirskyUtils app directory structure for the given app "
            "name in the current directory or optionally in the given "
            "directory.")

    def handle(self, app_name=None, target=None, **options):
        if app_name is None:
            raise CommandError("dummy, what's the app's name?")

        # Check that the app_name cannot be imported.
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError("%r conflicts with the name of an existing "
                               "Python module and cannot be used as an app "
                               "name. Please try another name." % app_name)
        
        if not options.get('template',None):
            options['template'] = os.path.join(mirskutils.__path__[0], 'conf/app_template')
        
        import itertools        
        exts = [options['extensions'], ['html','js','md','txt','css']]
        options['extensions'] = list(itertools.chain(*exts))
            
        super(Command, self).handle('app', app_name, target, **options)
