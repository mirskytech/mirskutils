import os
from django.core.management.templates import BaseCommand
import subprocess
from distutils.version import StrictVersion, LooseVersion
from optparse import make_option

import mirskutils

DEFAULT_PORT = 8000

class Command(BaseCommand):
    help = ("MirskyUtils running server ")

    option_list = BaseCommand.option_list + (
        make_option('-g','--enable-gevent', action="store_true", dest="gevent", help="gevent asyncronous loop in order to support cross-threading communication"),
        make_option('-s','--https', action="store_true", dest="https", help="forwards all requests to https protocol"),
        make_option('-m', '--module', action='store', type='string', dest='module')
        )


    def handle(self, port='', *args, **options):

        try:
            out = subprocess.check_output('uwsgi --version'.split(' '))
        except ImportError:
            print "uwsgi required but not installed"
            exit(1)
            
        if StrictVersion(out.strip()) < StrictVersion('1.9.4'):
            print "warning: this has only been tested against uwsgi v1.9.4"

        gevent_cmd = ''

        if options['gevent']:
        try:
            import gevent
        except ImportError:
            print "gevent required to run this set of uwsgi options"
            exit(1)
        
        if LooseVersion(gevent.__version__) < LooseVersion('1.0'):
            print "gevent 1.x required to run with uwsgi"
            exit(1)
            
                gevent_cmd = '--loop gevent --async 1000 --enable-threads --socket-timeout 30' if not options['gevent'] else ''
        
        self.port = port if port else DEFAULT_PORT        
        http_cmd = '--http-socket :%(port)s' % { 'port':self.port }
        if options['https']:
            http_cmd = '--http-to-https 127.0.0.1:8001'
            
        module_cmd = '--module wsgi' if not options['module'] else "--module %s" % options['module']
        
        
        command = 'uwsgi -M %s %s %s' % (gevent_cmd, http_cmd, module_cmd)
        #--http-socket :%(port)s --module wsgi --async 1000' % { 'port':self.port}
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        