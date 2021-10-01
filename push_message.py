import os

from channels.generic.http import AsyncHttpConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path


class PushMessage(AsyncHttpConsumer):
    async def handle(self, body: bytes) -> None:
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat.message",
                "text": "text_data",
            },
        )
        await self.send_response(
            200,
            b"Your response bytes",
            headers=[
                (b"Content-Type", b"text/plain"),
            ],
        )


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "push_message_settings")

application = ProtocolTypeRouter(
    {
        "http": URLRouter([
            path(r"push", PushMessage.as_asgi()),
            path(r"favicon.ico", PushMessage.as_asgi()),
        ]),
    }
)
