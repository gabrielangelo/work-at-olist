from django.db import models
from django.db.models import F, Q
from collections import defaultdict

# Create your models here.

def tree():
    return defaultdict(tree)


def dump_tree(t, path):
    for node in path:
        t = t[node]


def dicts(t):
    return {k.title: dicts(t[k]) for k in t}


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
                #node_queryset.create(title=parent.title, channel=parent.channel, lft=last_node.rgt + 1,
                                     #rgt=last_node.rgt + 2)
            else:
                node_queryset.filter(rgt__gt=root.lft, channel=root.channel).update(rgt=F('rgt') + 2)
                node_queryset.filter(lft__gt=root.lft, channel=root.channel).update(lft=F('lft') + 2)
                #node_queryset.create(title=parent.title, channel=parent.channel, lft=root.lft + 1, rgt=root.lft + 2)

    @classmethod
    def make_json_tree(cls, parent):
        interval = range(parent.lft, parent.rgt+1)
        nodes = cls.objects.filter(channel=parent.channel,
                                   rgt__in=interval, lft__in=interval
                                   ).order_by('lft')
        path = []
        root = nodes.first()
        size = nodes.count()
        path.append(root)
        t = tree()
        dump_tree(t, path)

        for i in range(1, size - 1):
            if nodes[i-1].lft == nodes[i].lft - 1:
                path.append(nodes[i])
                dump_tree(t, path)
                if i == size - 2:
                    path.append(nodes[i+1])
                    dump_tree(t, path)
                if nodes[i+1].lft == nodes[i].rgt + 2:
                    path.pop()
                    aux = nodes[i]
                    nodes = list(nodes) if not isinstance(nodes, list) else nodes
                    nodes[i] = nodes[i-1]
                    nodes[i-1] = aux
                    if i == size - 2:
                        path.append(nodes[i + 1])
                        dump_tree(t, path)
            elif nodes[i-1].rgt == nodes[i].lft - 1 and nodes[i+1].lft == nodes[i].rgt + 2:
                #path.pop()
                path.append(nodes[i])
                dump_tree(t, path)
                path.pop()
                path.pop()
                if i == size - 2:
                    path.append(nodes[i+1])
                    dump_tree(t, path)
            elif nodes[i-1].rgt == nodes[i].lft - 1:
                path.pop()
                path.append(nodes[i])
                dump_tree(t, path)
                path.pop()
                if i == size - 2:
                    path.append(nodes[i+1])
                    dump_tree(t, path)
            elif nodes[i+1].lft == nodes[i].lft + 1:
                path.append(nodes[i])
                dump_tree(t, path)

        return dicts(t)

