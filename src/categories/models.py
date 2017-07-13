from django.db import models
from django.db.models import F
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)
    channel = models.OneToOneField('channels.Channel', related_name='channel')
    rgt = models.IntegerField(default=1)
    lft = models.IntegerField(default=2)

    @classmethod
    def add_node(cls, root, parent):
            node_queryset = cls.objects.all()
            check_parents = node_queryset.filter(lft__gte=root.lft, rgt__lte=root.lft, channel=root.chanel)

            if check_parents.exists():
                node_queryset.filter(
                    lft__gt=root.rgt, rgt__gt=root.rgt,
                    channel=root.channel).update(rgt=F('rgt') + 2, lft=F('lft') + 2)

                node_queryset.create(title=parent.title, channel=parent.channel,
                                     rgt=root.rgt + 2, lft=root.lft + 1)
            else:
                node_queryset.filter(rgt__gt=root.rgt, lft__gt=root.lft).update(rgt=F('rgt')+2, lft=F('lft')+2)

                node_queryset.create(title=parent.title, channel=parent.channel,
                                     rgt=root.rgt + 2, lft=root.lft + 1)


