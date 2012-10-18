from django.db import models
from django.conf import settings

import accounts.models as accounts_models

class Video(models.Model):
    url = models.URLField(max_length=settings.URL_MAX_LENGTH)
    
class Rating(models.Model):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(accounts_models.User)
    rating = models.IntegerField()

