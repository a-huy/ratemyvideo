from django.db import models, DatabaseError
from base.managers import ActiveManager, VanishedManager
import django.utils.timezone

import datetime

class Base(models.Model):
    created_date = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    modified_date = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    deleted_date = models.DateTimeField(null=True, default=None, editable=False)

    objects = models.Manager()
    active = ActiveManager()
    vanished = VanishedManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.modified_date = django.utils.timezone.now()
        self.__save(*args, **kwargs)

    def vanish(self, *args, **kwargs):
        deleted_date = kwargs.pop('deleted_date', None) or django.utils.timezone.now()
        self.deleted_date = deleted_date
        self.__save(*args, **kwargs)

    def unvanish(self, *args, **kwargs):
        self.deleted_date = None
        self.__save(*args, **kwargs)

    def __save(self, *args, **kwargs):
        try:
            super(Base, self).save(*args, **kwargs)
        except DatabaseError, err:
            raise
