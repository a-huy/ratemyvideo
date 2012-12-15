import os

from globals import *
from constants import *

if 'andy' in map(lambda x: x.lower(), PROJECT_PATH.split(os.path.sep)) != -1:
    from local import *
else: from heroku import *