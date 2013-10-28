import os
from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand
from django.utils.crypto import get_random_string
from django.utils.importlib import import_module

import mirskutils


class Command(TemplateCommand):
    help = ("Creates a Django project directory structure for the given "
            "project name in the current directory or optionally in the "
            "given directory.")

    def handle(self, project_name=None, target=None, *args, **options):
        if project_name is None:
            raise CommandError("you must provide a project name")

        # Check that the project_name cannot be imported.
        try:
            import_module(project_name)
        except ImportError:
            pass
        else:
            raise CommandError("%r conflicts with the name of an existing "
                               "Python module and cannot be used as a "
                               "project name. Please try another name." %
                               project_name)
        
        if not options.get('template',None):
            options['template'] = os.path.join(mirskutils.__path__[0], 'conf/project_template')
        
        import itertools        
        exts = [options['extensions'], ['js','md','css']]
        options['extensions'] = list(itertools.chain(*exts))      
        
        super(Command, self).handle('project', project_name, target, **options)
        
        #prj_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),project_name)
        #repo = Repo.init(prj_path, bare=False)
        
        
