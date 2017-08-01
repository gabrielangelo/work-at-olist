from rest_framework.serializers import ModelSerializer
from categories.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id_category', 'lft', 'rgt')

    def to_representation(self, instance):
        objs = {'channel': instance.channel.description}
        objs['categories'] = self.Meta.model.make_json_tree(instance)
        return objs
