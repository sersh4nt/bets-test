from datetime import datetime, timedelta


class Timer:
    def __init__(self) -> None:
        self._started = False
        self._time_started = None

    def start(self) -> None:
        if self._started:
            raise ValueError("Timer already started!")
        self._started = True
        self._time_started = datetime.utcnow()

    def stop(self) -> timedelta:
        if not self._started:
            raise ValueError("Timer is not started!")
        self._started = False
        return datetime.utcnow() - self._time_started
