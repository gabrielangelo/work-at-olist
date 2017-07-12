from django.db import models
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)
    channel = models.OneToOneField('channels.Channel', related_name='channel')
    rgt = models.IntegerField()
    lft = models.IntegerField()

