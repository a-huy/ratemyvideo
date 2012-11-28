import json

from django.db import models
from django.conf import settings

import base.models as base_models
import accounts.models as accounts_models
import django.utils.timezone

class Video(base_models.Base):
    yt_id = models.CharField(max_length=settings.YT_ID_MAX_LENGTH, unique=True)
    title = models.CharField(max_length=settings.YT_TITLE_MAX_LENGTH)
    reward = models.DecimalField(max_digits=3, decimal_places=2)
    duration = models.IntegerField(default=0)

    def __unicode__(self):
        return self.yt_id + ' | ' + self.title + ' (' + str(duration) + ')'

class Rating(base_models.Base):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(accounts_models.User)
    rating = models.IntegerField()
    source_ip = models.IPAddressField()

    def __unicode__(self):
        return self.video + ' | ' + self.user + ' | ' + str(self.rating)

    def to_json(self):
        return json.dumps(self.json_safe())

    def json_safe(self):
        data = {
            'rating': self.rating
        }
        return data

class Vote(base_models.Base):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(accounts_models.User)
    like = models.BooleanField()
    source_ip = models.IPAddressField()

    def __unicode__(self):
        return self.video + ' | ' + self.user + ' | ' + ('like' if self.like else 'dislike')

class Question(base_models.Base):
    text = models.CharField(max_length=settings.QUESTION_MAX_LENGTH)
    video = models.ForeignKey(Video)
    time = models.IntegerField()

class Queue(base_models.Base):
    user = models.ForeignKey(accounts_models.User)
    video = models.ForeignKey(Video)
    bonuses = models.CharField(max_length=settings.VIDEO_BONUSES_MAX_LENGTH)
    expire_date = models.DateTimeField(default=django.utils.timezone.now)
