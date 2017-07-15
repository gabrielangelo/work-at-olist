from rest_framework.serializers import ModelSerializer
from channels.api.serializers import ChannelSerializer
from categories.models import Category


class CategorySerializer(ModelSerializer):
    channel = ChannelSerializer

    class Meta:
        model = Category
        fields = ('channel', )
        exclude = ('id', 'rgt', 'lft')
