from django.db import models


class TimerEvent(models.Model):
    class EventType(models.IntegerChoices):
        START = 0
        STOP = 1

    ts = models.DateTimeField(auto_now_add=True)
    timer_value = models.DateTimeField()
    type = models.IntegerField(choices=EventType.choices)

    class Meta:
        db_table = "timer_events"
