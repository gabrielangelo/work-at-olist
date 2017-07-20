from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from categories.models import Category
from channels.models import Channel
from categories.api.serializers import CategorySerializer
from .serializers import ChannelSerializer


class ChannelViewSet(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny, ]
    lookup_field = 'description'

    @detail_route(methods=['GET'], url_path='categories?')
    def categories(self, request, **kwargs):
        title = request.query_params.get('title', None)
        category = Category.objects.prefetch_related('channel').filter(
            channel=self.get_object(), title=title) if title else Category.objects.filter(lft=1,
                                                                                          channel=self.get_object())
        if category.exists():
            serializer = CategorySerializer(category.get())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
