from django.db import models
# Create your models here.
#
from workatolist.categories.models import Category


class Channel(models.Model):
    description = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        super(Channel, self).save(*args, **kwargs)
        Category.objects.create(title='category', channel=self)
