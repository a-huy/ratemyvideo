import json

from django.db import models
from django.conf import settings

import base.models as base_models

class User(base_models.Base):
    fb_id = models.CharField(max_length=settings.FB_ID_MAX_LENGTH)
    real_name = models.CharField(max_length=settings.REAL_NAME_MAX_LENGTH)
    earned = models.DecimalField(max_digits=5, decimal_places=2)
    rated = models.IntegerField()
    liked = models.IntegerField()
    commented = models.IntegerField()
    
    def to_json(self):
        return json.dumps(self.json_safe())
        
    def json_safe(self):
        data = {

        }

