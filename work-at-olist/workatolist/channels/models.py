from django.db import models
# Create your models here.
#
from workatolist.categories.models import Category


class Channel(models.Model):
    description = models.CharField(max_length=200)

    def create(self):
        Category.objects.create(title='category', channel=self)
        return super(self.__class__, self).objects.create()
