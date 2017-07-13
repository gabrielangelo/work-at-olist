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
            check_parents = node_queryset.filter(lft__gte=root.lft, rgt__lte=root.lft, channel=root.channel)

            if check_parents.exists():
                query_nodes = node_queryset.filter(Q(Q(lft__gt=root.rgt) | Q(rgt__gt=root.rgt)), channel=root.channel)
                query_nodes.update(rgt=F('rgt') + 2, lft=F('lft') + 2) if query_nodes.exists() else None

                node_queryset.create(title=parent.title, channel=parent.channel,
                                     rgt=root.rgt + 2, lft=root.lft + 1)
            else:
                query_nodes = node_queryset.filter(Q(Q(rgt__gt=root.lft) | Q(lft__gt=root.lft)), channel=root.channel)
                query_nodes.update(rgt=F('rgt')+2, lft=F('lft')+2) if query_nodes.exists() else None

                node_queryset.create(title=parent.title, channel=parent.channel,
                                     rgt=root.rgt + 2, lft=root.lft + 1)


