from django.db import models
from django.db.models import F
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)
    channel = models.OneToOneField('channels.Channel', related_name='channel')
    rgt = models.IntegerField()
    lft = models.IntegerField()

    @classmethod
    def add_node(cls, node, child=None, isroot=None):
            node_queryset = cls.objects.all()
            root = None

            if isroot and child is None:

                try:
                    root = node_queryset.get(title='category', channel=node.channel)
                except cls.DoesNotExist:
                    pass

                node_queryset.filter(
                    lft__gt=root.rgt, rgt__gt=root.rgt,
                    channel=node.channel).update(rgt=F('rgt') + 2, lft=F('lft') + 2)

                node_queryset.create(title=node.title, channel=node.channel,
                                     rgt=root.rgt + 2, lft=root.lft + 1)
            else:

                try:
                    root = node_queryset.get(title=node.title, channel=node.channel)
                except cls.DoesNotExist:
                    pass

                node_queryset.filter(rgt__gt=root.rgt, lft__gt=root.lft).update(rgt=F('rgt')+2, lft=F('lft')+2)

                node_queryset.create(title=child.title, channel=child.channel,
                                     rgt=root.rgt + 2, lft=root.lft + 1)

    @classmethod
    def del_node(cls, node):
        pass

