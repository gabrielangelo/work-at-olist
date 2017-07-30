from django.core.management.base import BaseCommand
from os.path import dirname, abspath
from django.db import transaction
from categories.models import Category
from channels.models import Channel
from csv import reader


class Command(BaseCommand):
    def add_arguments(self, parser):

        parser.add_argument(
            dest='channel',
            action='store',
            default=None
        )

        parser.add_argument(
            dest='file',
            action='store',
            default=None
        )

    def print_red(self, name):
        """red letter"""
        print("\033[91m {}\033[00m".format(name))

    def print_green(self, name):
        """grenn letter"""
        print('\033[92m'.format(name))

    def collect_categories(self, channel, file):
        """
        The channel and file parameters match the channel name and file, the file must be in the same directory as
        the manage.py file
        """
        format_file = 'csv'
        validate_format = True if format_file in file.split('.') else False

        if validate_format:
            base_file = dirname(dirname(dirname(dirname(abspath(__file__))))) + '/' + file
            query_channel, created = Channel.objects.get_or_create(description=channel)
            if not created:
                query_channel.channel.filter(channel=query_channel).delete()

            with open(base_file, 'r') as f:
                rows = reader(f)
                root = Category(title='Category', channel=query_channel)
                nodes = [root]
                parents = [nodes[0]]

                with transaction.atomic():
                    """
                    The existence of '/' is verified at each iteration in a row. If it does not exist, the root node is 
                    considered as the parent node of the node to be added, otherwise the previous node is fetched from 
                    parents and added as the parent node of the node to be added.
                    
                    Obs: parents is updated with each Category.add_nodes () call
                    """
                    for row in rows:
                        if row and '/' not in row[0] and row[0] != 'Category':
                            node = Category(title=row[0].strip(), parent=parents[0], channel=query_channel)
                            nodes.append(node)
                            nodes = Category.add_node(nodes=nodes)
                            self.print_red("Category: %s added" % nodes[-1].title)
                        elif row and '/' in row[0]:
                            parts = [p for p in row[0].split('/')]
                            size_parts = len(parts)

                            if size_parts > 2:
                                """ 
                                The loop begins at the end. The probability that a parent node is at the other end of 
                                the list is larger and makes the search less costly."""
                                parent = [i for i in nodes[::-1] if i.title == parts[:-1][-1].strip() and
                                          i.parent.title == parts[:-1][-2].strip()][0]
                            elif size_parts >= 2:
                                parent = [i for i in nodes[::-1] if i.title == parts[:-1][-1].strip()
                                          and i.parent == root][0]
                            else:
                                parent = nodes[0]

                            node = Category(title=parts[-1].strip(), parent=parent, channel=query_channel)
                            nodes.append(node)
                            nodes = Category.add_node(nodes=nodes)
                            parents.append(nodes[-1])

                            self.print_red("Category: %s added" % nodes[-1].title)

                    Category.persist_nodes(nodes)
        else:
            raise TypeError('Invalid File format')

    def handle(self, channel=None, file=None, **options):
        self.collect_categories(channel, file)
