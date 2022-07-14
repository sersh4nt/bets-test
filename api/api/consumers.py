import asyncio

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import TimerEvent
from .serializers import TimerEventSerializer
from .timer import timer


class TimerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("timer", self.channel_name)
        await self.accept()

        try:
            self.connections += 1
        except AttributeError:
            self.connections = 1
            self.update_task = asyncio.create_task(self.update_timer())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("timer", self.channel_name)

        self.connections -= 1
        if self.connections > 0:
            return

        self.update_task.cancel()
        self.update_task = None

    @database_sync_to_async
    def get_events(self):
        events = TimerEvent.objects.order_by("-ts")
        data = TimerEventSerializer(events, many=True).data
        return data

    async def update_timer(self):
        while True:
            events = await self.get_events()
            await self.channel_layer.group_send(
                "timer",
                {
                    "type": "timer_data",
                    "data": {
                        "events": events,
                        "value": timer.get_value(),
                        "is_running": timer.is_running(),
                    },
                },
            )
            await asyncio.sleep(0.5)

    async def timer_data(self, event):
        data = event["data"]
        await self.send_json(data)
