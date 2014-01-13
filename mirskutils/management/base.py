import sys
import json
import traceback

from django.core.management.base import BaseCommand, OutputWrapper

import argparse

class ArgumentError(Exception):
    pass

class ArgBaseCommand(BaseCommand):

    def add_arguments(self, parser):
        raise NotImplemented('please define an add_arguments method to your subclass')

    def create_parser(self, prog_name, subcommand):
        parser = argparse.ArgumentParser(prog="%s %s" %(prog_name,subcommand), usage=None, description=None)
        parser.add_argument('-t','--traceback', action="store_true")
        self.add_arguments(parser)
        return parser

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and Django settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr.
        """
        parser = self.create_parser(argv[0], argv[1])
        args = parser.parse_args(argv[2:])
        options = {'traceback':True}
        #handle_default_options(options) TODO : add default(s) eg. traceback
        try:
            self.execute(args)
        except ArgumentError as a:
            stderr = getattr(self, 'stderr', OutputWrapper(sys.stderr, self.style.ERROR))            
            parser.error(a.message)
            sys.exit(1)
        except Exception as e:
            # self.stderr is not guaranteed to be set here
            stderr = getattr(self, 'stderr', OutputWrapper(sys.stderr, self.style.ERROR))
            if getattr(args, 'traceback', False):
                stderr.write(traceback.format_exc())
            else:
                stderr.write('%s: %s' % (e.__class__.__name__, e))
            sys.exit(1)	