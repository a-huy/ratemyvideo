import sys, os

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(SCRIPT_PATH[:SCRIPT_PATH.rfind('scripts/')])

from django.core.management import setup_environ
from ratemyvideo import settings
setup_environ(settings)

