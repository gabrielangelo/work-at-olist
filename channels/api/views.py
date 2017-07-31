from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from categories.models import Category
from channels.models import Channel
from categories.api.serializers import CategorySerializer
from .serializers import ChannelSerializer


class ChannelViewSet(ReadOnlyModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'description'