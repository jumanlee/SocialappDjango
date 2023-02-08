#similar to url file but for websockets

from django.urls import re_path

# This is much like the way we import our views so that we send our requests to various routes to the appropriate code.
from . import consumers

websocket_urlpatterns = [
    # Let's get a response to a regular expression, so any URL that includes WS for WebSockets. So if you can't really use the API for our REST API, and I'm going to use WS for the URLs for our WebSockets. And then we're going to capture any string after WS, that's going to be the room name. Then we're going to send anything like this that we capture through our chat consumer code. So it's going to be in our consumers file, we're going to have a class called chat consumer.
    re_path(r'ws/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi())
]