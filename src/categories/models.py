from django.db import models
from django.db import transaction
from .nested_tree import *
import uuid
# Create your models here.


class Category(models.Model):
    """
    Each node will have two lft and rgt fields which will be the extreme points of their intervals. 
    The lft and rgt fields of their child nodes are within the range of the parent node.
    """
    id_category = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    channel = models.ForeignKey('channels.Channel', related_name='channel', on_delete=models.CASCADE)
    rgt = models.IntegerField(default=2)
    lft = models.IntegerField(default=1)
    parent = models.ForeignKey('categories.Category', related_name='parent_node', null=True)

    class Meta:
        ordering = ['lft', ]

    def __repr__(self):
        return '{0} {1}: {2}'.format(self.lft, self.rgt, self.title)

    @classmethod
    def add_node(cls, nodes):
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
        rgt_parent = nodes[-1].parent.rgt
        lft_parent = nodes[-1].parent.lft
        last_node = None
        node = nodes[-1]
        for child in nodes[:-1]:
            child.rgt = child.rgt + 2 if child.rgt >= rgt_parent else child.rgt
            child.lft = child.lft + 2 if child.lft > rgt_parent else child.lft
            last_node = child if child.rgt == rgt_parent - 1 else last_node

        if last_node:
            node.lft = last_node.rgt + 1
            node.rgt = last_node.rgt + 2
        else:
            node.lft = lft_parent + 1
            node.rgt = lft_parent + 2

        return nodes

    @classmethod
    def persist_nodes(cls, nodes):
        cls.objects.bulk_create(nodes)
        print('OK')

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
                                   ).order_by('lft','title')

        path = [] if parent.parent_id is None else [nodes.first()]#the path is used to create the hierarchies in dump_tree method
        t = tree()
        for node in nodes:

            if node.parent_id is None or node.parent_id == path[-1].id_category:#check if a node is a child of another node that is in path
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
                while node.parent_id != path[-1].id_category:
                    path.pop()
                path.append(node)
                dump_tree(t, path)

        return dicts(t)
