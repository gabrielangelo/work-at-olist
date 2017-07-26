from django.db import models
from django.db.models import F
from .nested_tree import *
# Create your models here.


class Category(models.Model):
    """
    Each node will have two lft and rgt fields which will be the extreme points of their intervals. 
    The lft and rgt fields of their child nodes are within the range of the parent node.
    """
    title = models.CharField(max_length=50)
    channel = models.ForeignKey('channels.Channel', related_name='channel')
    rgt = models.IntegerField(default=2)
    lft = models.IntegerField(default=1)
    parent = models.ForeignKey('categories.Category', related_name='parent_node', null=True)

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.lft, self.rgt, self.title)

    @classmethod
    def add_node(cls, parent, node):
            """
            Add nodes on the tree. First it checks if the parent node contains child nodes, if 
            it has, the nodes with the fields lft and rgt larger than the rgt field of the parent 
            node will be incremented by 2, then the last node added within the subset of child nodes 
            will be fetched And the lft and rgt fields of the node to be added will be incremented by 
            parent.lft + 1 and parent.rgt + 2.If the parent node does not contain child nodes, the 
            nodes with the lft and rgt fields larger than the lft field of the parent node are 
            incremented by 2, and the lft and rgt fields are incremented by parent.lft + 1 and 
            parent.rgt + 2.
            """
            node_queryset = cls.objects.prefetch_related('channel').all()
            interval = range(parent.lft, parent.rgt + 1)
            check_parents = node_queryset.filter(
                rgt__in=interval,
                lft__in=interval, channel=parent.channel).exclude(id=parent.id)
            if check_parents.exists():
                node_queryset.filter(rgt__gte=parent.rgt, channel=parent.channel).update(rgt=F('rgt') + 2)
                node_queryset.filter(lft__gt=parent.rgt, channel=parent.channel).update(rgt=F('lft') + 2)
                last_node = check_parents.filter(rgt=parent.rgt - 1).get()
                node_queryset.create(title=node.title, channel=node.channel, lft=last_node.rgt + 1,
                                     rgt=last_node.rgt + 2, parent=parent)
            else:
                node_queryset.filter(rgt__gt=parent.lft, channel=parent.channel).update(rgt=F('rgt') + 2)
                node_queryset.filter(lft__gt=parent.lft, channel=parent.channel).update(lft=F('lft') + 2)
                node_queryset.create(title=node.title, channel=node.channel, lft=parent.lft + 1, rgt=parent.lft + 2,
                                     parent=parent)

    @classmethod
    def make_json_tree(cls, parent):
        """
         Creates a json structure that returns the category hierarchy. First, the function receives the parent node as 
         the starting point and then returns an ordered list of the child nodes of the parent node. The tree is covered 
         with the following considerations:
               - With each interaction the path can be to have an element added or removed;
               - If a node is a child of the previous one it is incremented in the path and in the tree;
               - If a node is a sibling of the previous node the last node of the path (its brother) is removed and the 
path returns to the parent node of the siblings;
               - If a node is one level above the previous node, the last two nodes of the path are removed by returning
 to the root node of the leaf;
               - If a node is a higher level than the previous node, the tree nodes of the tree are traversed until it 
reaches the node node of the current node.

Note: - The path works like a stack and its operations are O(1).
         - The tree is covered once.
         - The highest cost is the return of the ordered list of nodes.
         - This method is used in category serializer.
        """
        if parent is None:
            return None

        interval = range(parent.lft, parent.rgt+1)
        nodes = cls.objects.filter(channel=parent.channel,
                                   rgt__in=interval, lft__in=interval
                                   ).order_by('lft')

        path = [] if parent.parent_id is None else [nodes.first()]#the path is used to create the hierarchies in dump_tree method
        t = tree()
        for node in nodes:

            if node.parent_id is None or node.parent_id == path[-1].id:#check if a node is a child of another node that is in path
                path.append(node)
                dump_tree(t, path)

            elif node.lft == path[-1].rgt + 1:#check if a node is brother of the last node in path
                path.pop()
                path.append(node)
                dump_tree(t, path)

            elif node.lft == path[-1].rgt + 2:#check if a node is one level of the other
                path.pop()
                path.pop()
                path.append(node)
                dump_tree(t, path)

            elif node.lft > path[-1].rgt + 2:#Check if the level of one node is greater than the other n times
                while node.parent_id != path[-1].id:
                    path.pop()
                path.append(node)
                dump_tree(t, path)

        return dicts(t)

