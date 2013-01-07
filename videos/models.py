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
    tags = models.CharField(max_length=settings.VIDEO_TAGS_MAX_LENGTH, default='')

    def __unicode__(self):
        return self.yt_id + ' | ' + self.title + ' (' + str(self.duration) + ')'

class Rating(base_models.Base):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(accounts_models.User)
    rating = models.IntegerField()
    bonuses = models.CharField(max_length=settings.VIDEO_BONUSES_MAX_LENGTH)
    source_ip = models.IPAddressField()

    def __unicode__(self):
        return str(self.video) + ' | ' + str(self.user) + ' | ' + str(self.rating)

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
        return str(self.video) + ' | ' + str(self.user) + ' | ' + ('like' if self.like else 'dislike')

class Comment(base_models.Base):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(accounts_models.User)
    text = models.CharField(max_length=settings.VIDEO_COMMENTS_MAX_LENGTH)
    source_ip = models.IPAddressField()

class Question(base_models.Base):
    text = models.CharField(max_length=settings.QUESTION_MAX_LENGTH)
    video = models.ForeignKey(Video)
    time = models.IntegerField()

class Queue(base_models.Base):
    user = models.ForeignKey(accounts_models.User)
    video = models.ForeignKey(Video)
    bonuses = models.CharField(max_length=settings.VIDEO_BONUSES_MAX_LENGTH)
    expire_date = models.DateTimeField(default=django.utils.timezone.now)

    def __unicode__(self):
        return str(self.video) + ' | ' + str(self.user) + ' | (' + str(self.expire_date) + ') : ' + \
            (self.bonuses if self.bonuses else 'none')
