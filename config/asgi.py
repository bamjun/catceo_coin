# import os

# from django.core.asgi import get_asgi_application

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from chat.routing import websocket_urlpatterns


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# application = get_asgi_application()


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })

import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
application = get_default_application()
