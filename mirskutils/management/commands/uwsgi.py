import os
from django.core.management.templates import BaseCommand
import subprocess

import mirskutils

DEFAULT_PORT = 8000

class Command(BaseCommand):
    help = ("MirskyUtils running server ")

    option_list = BaseCommand.option_list + (
        )


    def handle(self, port='', *args, **options):
        
        self.port = port if port else DEFAULT_PORT
        
        command = 'uwsgi -M --loop gevent --http-socket :%(port)s --module wsgi --async 1000' % { 'port':self.port}
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        