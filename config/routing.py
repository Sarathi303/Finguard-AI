from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from fraud import consumers

websocket_urlpatterns = [
    re_path(r'ws/fraud-feed/$', consumers.DashboardConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
},)