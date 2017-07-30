from django.db import models
# Create your models here.
#
from categories.models import Category


class Channel(models.Model):
    description = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['description', ]

    def __repr__(self):
        return '%s' % self.description