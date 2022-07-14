from rest_framework import serializers
from .models import TimerEvent


class TimerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerEvent
        exclude = ["id"]
