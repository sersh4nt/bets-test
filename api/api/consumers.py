import asyncio

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import TimerEvent
from .serializers import TimerEventSerializer
from .timer import timer


class TimerConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.connections += 1
        except AttributeError:
            self.connections = 1
            self.update_task = asyncio.ensure_future(self.update_timer())

        await self.channel_layer.group_add("timer", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("timer", self.channel_name)

        self.connections -= 1
        if self.connections > 0:
            return

        self.update_task.cancel()
        self.update_task = None

    async def update_timer(self):
        while True:
            events = TimerEvent.objects.all()
            events_data = TimerEventSerializer(events).data

            await self.channel_layer.group_send(
                "timer",
                {
                    "type": "timer_data",
                    "data": {
                        "events": events_data,
                        "value": timer.get_value(),
                        "is_running": timer.is_running(),
                    },
                },
            )
            await asyncio.sleep(0.5)

    async def timer_data(self, event):
        data = event["data"]
        await self.send_json(data)
