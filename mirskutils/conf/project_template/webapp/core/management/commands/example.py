
from django.core.management.base import BaseCommand
from mirskutils.management.base import ArgBaseCommand



# For use with django defaults (deprecated python optparser)
#class Command(BaseCommand):
#
#    #astring = make_option('-a', '--aaaa', action="store", type="string", dest="aaa_variable")
#    #bboolean = make_option('-b', '--bbbb', action="store_true", type="string", dest="bbb_variable")
#
#    #option_list = BaseCommand.option_list + (astring,bbooleans)
#
#    def handle(self, *arguments, **options):
#        pass


class Command(ArgBaseCommand):
	
	def add_arguments(self, argparser):
		
		# flag arguments
		group = argparser.add_mutually_exclusive_group(required=True)
		group.add_argument('-a','--letterA') # arguments.letterA
		group.add_argument('-b','--letterC') # arguments.letterB
		
		# positional arguments
		argparser.add_argument('C')	# arguments.C
		argparser.add_argument('D')	
			
	def handle(self, arguments):
		pass
		
