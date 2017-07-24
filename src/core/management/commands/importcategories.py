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
            (
                Category.objects.prefetch_related('channel').filter(
                    channel=query_channel.get()).exclude(title='Category').delete(),
                Category.objects.prefetch_related('channel').filter(channel=query_channel.get()).update(lft=1, rgt=2)
                if query_channel.exists() else
                Channel.objects.create(description=channel)
            )
            with open(base_file, 'r') as f:
                    rows = reader(f)
                    for row in rows:
                            if row and '/' in row[0]:
                                    parts = [p for p in row[0].split('/')]
                                    parent = Category.objects.get(title=parts[:-1][-1].strip(),
                                                                  channel=query_channel.get(),
                                                                  parent__title='Category'
                                                                  if parts[0].strip() == parts[:-1][-1].strip() else
                                                                  parts[:-1][-2].strip()
                                                                  )

                                    node = Category(title=parts[-1:][0].strip(), channel=query_channel.get())
                                    Category.add_node(parent, node)
                            elif row and '/' not in row[0] and row[0] != 'Category':
                                    root = Category.objects.get(title='Category', channel=query_channel.get())
                                    Category.add_node(root,
                                                      Category(title=row[0], channel=query_channel.get()))
                    print(len(connection.queries))
                            # else:
                            #     raise Exception('Error file')


        # format_file = 'csv'
        # validate_format = True if format_file in file.split('.') else False

        #if validate_format:
            #base_file = dirname(dirname(dirname(dirname(abspath(__file__))))) + '/' + file
            # query_channel = Channel.objects.filter(description=channel)
            # (Category.objects.filter(channel=query_channel.get()).delete() if query_channel.exists() else
            #  Channel.objects.create(description=channel))
            #
            # with open(file, 'r') as f:
            #     rows = reader(f)
            #     root = 'Category'

                #for row in rows:
                    # if row and '/' not in row[0] and row[0] == root:
                        # Category.add_node(Category(title=root, channel=query_channel.get()),
                        #                   Category(title=row[0], channel=query_channel.get()))
                    # if row and '/' not in row[0] and row[0] != root:
                    #     root = Category(title=root, channel__description=channel)
                    #     Category.add_node(root, Category(title=row[0], channel=query_channel.get()))
                    #
                    # elif row and '/' in row[0]:
                    #     parts = [p for p in row[0].split('/')]
                    #     root = Category.objects.filter(title=parts[:-1][-1], channel__description=channel)
                    #     Category.add_node(root.get(), Category(title=parts[-1:], channel=query_channel.get()))


                    #elif row and
                    # else:
                    #     raise Exception('Error file')

                #Category.objects.bulk_create(categories)
        else:
            raise TypeError('Invalid File format')

    def handle(self, channel=None, file=None, **options):
            self.collect_categories(channel, file)


