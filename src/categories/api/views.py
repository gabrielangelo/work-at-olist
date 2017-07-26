from django.http import Http404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from categories.models import Category
from categories.api.serializers import CategorySerializer
from rest_framework.filters import DjangoFilterBackend


class CategoriesViewset(ReadOnlyModelViewSet):
    """filter categories by description's channel"""
    lookup_field = 'channel__description'
    permission_classes = [AllowAny, ]
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('title', 'channel__description')

    class Meta:
        model = Category

    def get_queryset(self):
        channel = self.request.query_params.get('channel__description', None)
        title = self.request.query_params.get('title', None)
        if title and channel:
            queryset = self.Meta.model.objects.prefetch_related('channel').filter(channel__description=channel,
                                                                                  title=title)
            if not queryset.exists():
                raise Http404
            return queryset

        elif channel:
            queryset = self.Meta.model.objects.prefetch_related('channel').filter(lft=1, channel__description=channel)
            if not queryset.exists():
                raise Http404
            return queryset
        elif title:
            queryset = self.Meta.model.objects.prefetch_related('channel').filter(title=title)
            if not queryset.exists():
                raise Http404
            return queryset
        else:
            return self.Meta.model.objects.prefetch_related('channel').filter(lft=1)

    def list(self, request, *args, **kwargs):
        '''
        filter categories by title and/or channel description. If 
        a category is filtered only by title, categories with 
        this title(if exists) can be sought on all channels. If the same 
        is filtered only by channel, all categories from this channel(if exists), 
        will be sought. If the two query parameters coexist, one category(if exists)
        with her subcategories of a channel will be sought.
        All data are organized by a json hierarchical structure 
        '''
        return super(self.__class__, self).list(request, *args, **kwargs)
