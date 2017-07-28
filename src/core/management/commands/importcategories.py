from django.core.management.base import BaseCommand
from os.path import dirname, abspath
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

    def collect_categories(self, channel, file):
        from django.db import connection
        format_file = 'csv'
        validate_format = True if format_file in file.split('.') else False

        if validate_format:
            base_file = dirname(dirname(dirname(dirname(abspath(__file__))))) + '/' + file
            query_channel = Channel.objects.filter(description=channel)

            if query_channel.exists():
                # if a channel exists, delete all you categories, else a new channel is created with your default category
                Category.objects.prefetch_related('channel').filter(
                    channel=query_channel.get()).exclude(title='Category').delete()
                Category.objects.prefetch_related('channel').filter(channel=query_channel.get()).update(lft=1, rgt=2)

            else:
                Channel.objects.create(description=channel)

            with open(base_file, 'r') as f:
                rows = reader(f)
                out_nodes = Category.objects.prefetch_related('channel').filter(
                    channel__description=channel).order_by('lft')
                root = out_nodes.first()
                parents = [root]
                # with transaction.atomic():
                for row in rows:
                    if row and '/' in row[0]:
                        parts = [p for p in row[0].split('/')]
                        # get the parent node in parts list
                        check_parents = [i for i in parents[::-1] if i['description'] == parts[:-1][-1].strip()
                                         and i['parent__description'] == parts[:-1][-2].strip()]

                        node = Category(title=parts[-1:][0].strip(), channel=query_channel.get())

                        parent = (check_parents.pop() if check_parents else
                                  Category.objects.filter(title=parts[:-1][-1].strip(),
                                                          channel=query_channel.get(),
                                                          parent__title=parts[:-1][-2].strip()
                                                          ).values(
                                      'id', 'lft', 'rgt', 'description', 'parent__title'))
                        parents.append(parent)
                        Category.add_node(parent, node, out_nodes)

                    elif row and '/' not in row[0] and row[0] != 'Category':
                        Category.add_node(root,
                                          Category(title=row[0], channel=query_channel.get()))

                print('%d de teste' % len(connection.queries))
        else:
            raise TypeError('Invalid File format')

    def handle(self, channel=None, file=None, **options):
        self.collect_categories(channel, file)
