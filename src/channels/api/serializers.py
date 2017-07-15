from rest_framework import serializers
from channels.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        exclude = ('id',)
