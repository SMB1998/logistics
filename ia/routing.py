from django.urls import re_path
from .consumers import IAConsumer

websocket_urlpatterns = [
    re_path(r'ws/ia/$', IAConsumer.as_asgi()),
]
