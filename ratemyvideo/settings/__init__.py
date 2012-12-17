import os

from global_settings import *
from constants import *


if 'andy' in map(lambda x: x.lower(), PROJECT_PATH.split(os.path.sep)):
    from local import *
else:
    try:
        tag = os.environ['ENV_TAG']
        if tag == 'test': from test import *
        else: from heroku import *
    except: from heroku import *
