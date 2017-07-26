from rest_framework.serializers import ModelSerializer
from categories.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', 'lft', 'rgt')

    def to_representation(self, instance):
        return self.Meta.model.make_json_tree(instance)
