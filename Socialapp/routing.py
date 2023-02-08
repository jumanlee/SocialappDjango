from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# So now we're just defining a WebSocket, a new WebSocket, that will direct to our chat application.
# That's going to be an instance of URL router, and it's going to be configured to in our chat client in the routing file, there's going to be a Python list called WebSocket URL patterns. This is going to be just like the URL patterns we've already seen for the various URLs files. So we can close this. We can turn our attention to our chat client. And we can open the routing for the actual chat client, and so this should be a blank document. And this is going to look very much like the URLs type, URLs patterns that we've already seen.
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
    
})