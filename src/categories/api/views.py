from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
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
    queryset = Category.objects.filter(lft=1)

    class Meta:
        model = Category

    def get_queryset(self):
        filter = {}
        query_params_size = len(self.request.query_params)
        if query_params_size > 0:
            for field in self.filter_fields:
                param = self.request.query_params.get(field, None)
                if param:
                    filter[field] = param
                else:
                    pass
            if 'channel__description' in filter.keys() and query_params_size == 1:
                filter['lft'] = 1
                self.Meta.model.objects.filter(**filter)

            queryset = self.Meta.model.objects.filter(**filter)
            if not queryset.exists():
                raise Http404
            return queryset
        return self.queryset

    def list(self, request, *args, **kwargs):
        """
        filter categories by title and/or channel description. If
        a category is filtered only by title, categories with
        this title(if exists) can be sought on all channels. If the same
        is filtered only by channel, all categories from this channel(if exists),
        will be sought. If the two query parameters coexist, one category(if exists)
        with her subcategories of a channel will be sought.
        All data are organized by a json hierarchical structure
        """
        return super(self.__class__, self).list(request, *args, **kwargs)
