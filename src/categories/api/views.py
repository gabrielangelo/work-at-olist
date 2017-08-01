from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from categories.models import Category
from .serializers import CategorySerializer
from .mixins import MultiplesQueriesMixin
from rest_framework.filters import DjangoFilterBackend


class CategoriesViewset(MultiplesQueriesMixin, ReadOnlyModelViewSet):
    """filter categories by description's channel"""
    lookup_field = 'channel__description'
    permission_classes = [AllowAny, ]
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('title', 'channel__description')
    queryset = Category.objects.filter(lft=1)

    class Meta:
        model = Category

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
