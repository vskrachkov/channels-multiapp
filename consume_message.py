import os

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url


class MessageConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self) -> None:
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def chat_message(self, event: dict) -> None:
        await self.send_json(event)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "consumer_message_settings")

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter([url(r"ws/", MessageConsumer.as_asgi())]),
    }
)
