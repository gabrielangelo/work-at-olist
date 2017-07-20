from rest_framework.routers import SimpleRouter
from channels.api.views import ChannelViewSet

router_v1 = SimpleRouter(trailing_slash=False)
router_v1.register('channels', ChannelViewSet, base_name='channels')

