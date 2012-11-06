import json

from django.db import models
from django.conf import settings

import base.models as base_models

class User(base_models.Base):
    fb_id = models.CharField(max_length=settings.FB_ID_MAX_LENGTH)
    real_name = models.CharField(max_length=settings.REAL_NAME_MAX_LENGTH)
    email = models.EmailField(max_length=settings.EMAIL_MAX_LENGTH)
    earned = models.DecimalField(max_digits=5, decimal_places=2, default=00.00)
    rated = models.IntegerField(default=0)
    liked = models.IntegerField(default=0)
    commented = models.IntegerField(default=0)
    subscribed = models.IntegerField(default=0)
    location = models.CharField(max_length=settings.LOCATION_MAX_LENGTH)
    age = models.IntegerField(default=0)
    karma = models.IntegerField(default=0)
    gender = models.CharField(max_length=settings.GENDER_MAX_LENGTH)

    def to_json(self):
        return json.dumps(self.json_safe())
        
    def json_safe(self):
        data = {
            'fb_id': self.fb_id,
            'real_name': self.real_name,
            'earned': str(self.earned),
            'rated': self.rated,
            'liked': self.liked,
            'commented': self.commented,
            'location': self.location,
            'age': self.age,
            'karma': self.karma,
            'email': self.email,
            'subscribed': self.subscribed,
            'gender': self.gender
        }
        return data

class InviteRequest(base_models.Base):
    name = models.CharField(max_length=settings.REAL_NAME_MAX_LENGTH)
    email = models.EmailField(max_length=settings.EMAIL_MAX_LENGTH)
    description = models.CharField(max_length=settings.DESC_MAX_LENGTH)

