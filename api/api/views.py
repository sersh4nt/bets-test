from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from .models import TimerEvent
from .timer import timer

@api_view(["POST"])
@permission_classes([AllowAny])
def post_event(request: Request) -> Response:
    if timer.is_running():
        value = timer.stop()
        TimerEvent.objects.create(timer_value=value, type=TimerEvent.EventType.STOP)
    else:
        timer.start()
        TimerEvent.objects.create(type=TimerEvent.EventType.START)

    return Response({"is_running": timer.is_running()}, status=201)
