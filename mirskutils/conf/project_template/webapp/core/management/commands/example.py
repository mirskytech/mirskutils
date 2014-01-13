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


# uses newer pythong argparser (does not support default options like traceback and no-input, yet)

#from mirskutils.management.base import ArgBaseCommand
#class Command(ArgBaseCommand):
        
        #def add_arguments(self, argparser):
                #group = argparser.add_mutually_exclusive_group(required=True)   
                #group.add_argument('-a','--aa')
                #group.add_argument('-b','--bb')
                #argparser.add_argument('position1')
                #argparser.add_argument('position2') 
                        
        #def handle(self, arguments):
            
            #mutually_exclusive = getattr(arguments,'aa', getattr(arguments,'bb'))
            #position_arg_1 = arguments.position1
            
            
