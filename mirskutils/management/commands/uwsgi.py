import os
from django.core.management.templates import BaseCommand
import subprocess

import mirskutils



class Command(BaseCommand):
    help = ("MirskyUtils running server ")

    def handle(self, app_name=None, target=None, **options):
        command = 'uwsgi -M --http :8000 --module wsgi --gevent 30'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        