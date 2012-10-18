#!/usr/bin/env python
from django.core.management import execute_manager
try:
    import herpderp.settings
except ImportError:
    import sys
    sys.stderr.write("Error: Cannot find the file 'settings.py' in the directory containing %r.\nIt appears you have customized things.\nYou will have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it is causing an ImportError.)\n" % __file__)
    sys.exit(1)
   
if __name__ == '__main__':
    execute_manager(herpderp.settings)

