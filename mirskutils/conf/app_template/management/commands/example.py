
from django.core.management.base import BaseCommand



class Command(BaseCommand):

    #astring = make_option('-a', '--aaaa', action="store", type="string", dest="aaa_variable")
    #bboolean = make_option('-b', '--bbbb', action="store_true", type="string", dest="bbb_variable")

    #option_list = BaseCommand.option_list + (astring,bbooleans)

    def handle(self, *arguments, **options):
        pass
    
    
