from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
from routers import router_v1

schema_view = get_swagger_view(title='Work at on Olist')

urlpatterns = [
    url(r'^docs', schema_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router_v1.urls)),
    url(r'^$', schema_view)
    #url(r'^docs/', include('rest_framework_swagger.urls'))
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
