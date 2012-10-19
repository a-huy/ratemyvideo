from django.db import models

class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(deleted_date=None)

class VanishedManager(models.Manager):
    def get_query_set(self):
        return super(VanishedManager, self).get_query_set().exclude(deleted_date=None)

