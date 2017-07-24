from os.path import dirname, abspath

from .models import Category
from channels.models import Channel
from csv import reader


def prefix(channel, file):

        format_file = 'csv'
        validate_format = True if format_file in file.split('.') else False

        if validate_format:
            base_file = dirname(dirname(abspath(__file__))) + file
            query_channel = Channel.objects.filter(description=channel)
            (Category.objects.filter(channel=query_channel.get()).delete() if query_channel.exists() else
             Channel.objects.create(description=channel))

            with open(base_file, 'rb') as f:
                    rows = reader(f)
                    root = 'Category'
                    node = None
                    categories = []
                    for row in rows:
                            if row and '/' in row[0]:
                                    parts = [p for p in row[0].split('/')]
                                    root = Category.objects.get(title=parts[:-1][-1], channel=query_channel.get())
                                    node = parts[-1:]
                                    categories.append(Category.add_node(root, node[0]))
                            elif row and '/' not in row[0] and row[0] != root:
                                    categories.append(Category.add_node(root, node))
                            else:
                                raise Exception('Error file')

                    #Category.objects.bulk_create(categories)
        else:
            raise TypeError('Invalid File format')




if __name__ == '__main__':

    ROOT_DIR = dirname(dirname(abspath(__file__)))
    print(type(ROOT_DIR))
    print('oi')


