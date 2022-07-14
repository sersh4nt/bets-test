from datetime import datetime


class Timer:
    def __init__(self) -> None:
        self._started = False
        self._time_started = datetime.utcnow()

    def start(self) -> None:
        if self._started:
            raise ValueError("Timer is already started!")
        self._started = True
        self._time_started = datetime.utcnow()

    def stop(self) -> float:
        if not self._started:
            raise ValueError("Timer is not started!")
        self._started = False
        return (datetime.utcnow() - self._time_started).total_seconds()

    def is_running(self) -> bool:
        return self._started
