from django.db import models
from django.conf import settings

import base.models as base_models
import accounts.models as accounts_models

class Video(base_models.Base):
    yt_id = models.CharField(max_length=settings.YT_ID_MAX_LENGTH)
    reward = models.DecimalField(max_digits=3, decimal_places=2)
    
    def __unicode__(self):
        return self.yt_id
    
class Rating(base_models.Base):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(accounts_models.User)
    rating = models.IntegerField()
    
    def __unicode__(self):
        return self.video + '|' + str(self.rating)
    
class Question(base_models.Base):
    text = models.CharField(max_length=settings.QUESTION_MAX_LENGTH)
    video = models.ForeignKey(Video)
    time = models.IntegerField()

