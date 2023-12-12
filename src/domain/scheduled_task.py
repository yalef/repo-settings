import dataclasses
import typing

from .schedule import Schedule


@dataclasses.dataclass
class ScheduledTask:
    id: str
    func: typing.Callable
    kwargs: dict[str, typing.Any]
    schedule: Schedule
