from django.db import models
from django.db.models import F, Q


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)
    channel = models.ForeignKey('channels.Channel', related_name='channel')
    rgt = models.IntegerField(default=2)
    lft = models.IntegerField(default=1)

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.lft, self.rgt, self.title)

    @classmethod
    def add_node(cls, root, parent):
            node_queryset = cls.objects.all()
            check_parents = node_queryset.filter(
                rgt__in=range(root.lft, root.rgt+1),
                lft__in=range(root.lft, root.rgt+1), channel=root.channel).exclude(id=root.id)

            if check_parents.exists():
                node_queryset.filter(rgt__gte=root.rgt, channel=root.channel).update(rgt=F('rgt') + 2)
                node_queryset.filter(lft__gt=root.rgt, channel=root.channel).update(rgt=F('lft') + 2)
                last_node = check_parents.last()
                node_queryset.create(title=parent.title, channel=parent.channel, lft=last_node.rgt + 1,
                                     rgt=last_node.rgt + 2)
            else:
                node_queryset.filter(rgt__gt=root.lft, channel=root.channel).update(rgt=F('rgt') + 2)
                node_queryset.filter(lft__gt=root.lft, channel=root.channel).update(lft=F('lft') + 2)
                node_queryset.create(title=parent.title, channel=parent.channel, lft=root.lft + 1, rgt=root.lft + 2)

