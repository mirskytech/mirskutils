#!/Users/andrew/env/infogem/bin/python
import sys

from django.core import management
from django.conf import settings


if __name__ == "__main__":
    
    
    if len(sys.argv) > 1 and sys.argv[1] == 'startproject':
        from mirskutils.management.commands.startproject import Command
        newproject = Command()
        newproject.run_from_argv(sys.argv)
    else:
        management.execute_from_command_line()
