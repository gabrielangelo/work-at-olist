from django.db import models
from django.db.models import F
from .nested_tree import *
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)
    channel = models.ForeignKey('channels.Channel', related_name='channel')
    rgt = models.IntegerField(default=2)
    lft = models.IntegerField(default=1)
    parent = models.ForeignKey('categories.Category', related_name='parent_node', null=True)

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
                last_node = check_parents.filter(rgt=root.rgt-1).get()
                node_queryset.create(title=parent.title, channel=parent.channel, lft=last_node.rgt + 1,
                                     rgt=last_node.rgt + 2, parent=root)
            else:
                node_queryset.filter(rgt__gt=root.lft, channel=root.channel).update(rgt=F('rgt') + 2)
                node_queryset.filter(lft__gt=root.lft, channel=root.channel).update(lft=F('lft') + 2)
                node_queryset.create(title=parent.title, channel=parent.channel, lft=root.lft + 1, rgt=root.lft + 2,
                                     parent=root)

    @classmethod
    def make_json_tree(cls, parent):
        if parent is None:
            return None

        interval = range(parent.lft, parent.rgt+1)
        nodes = cls.objects.filter(channel=parent.channel,
                                   rgt__in=interval, lft__in=interval
                                   ).order_by('lft')

        path = [] if parent.parent_id is None else [nodes.first()]
        t = tree()
        for node in nodes:
            if node.parent_id is None or node.parent_id == path[-1].id:
                path.append(node)
                dump_tree(t, path)
                # if node.lft == path[-1].rgt + 2:
            elif node.lft == path[-1].rgt + 1:
                path.pop()
                path.append(node)
                dump_tree(t, path)
            elif node.lft == path[-1].rgt + 2:
                path.pop()
                path.pop()
                path.append(node)
                dump_tree(t, path)
            elif node.lft > path[-1].rgt +2:
                while node.parent_id != path[-1].id:
                    path.pop()
                path.append(node)
                dump_tree(t, path)

        return dicts(t)

