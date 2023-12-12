import typing

from .schedule import Schedule
from .scheduled_task import ScheduledTask


class ScheduledTaskService:
    def create_task(
        self,
        task_id: str,
        func: typing.Callable,
        kwargs: dict[str, typing.Any],
        schedule: Schedule,
    ) -> ScheduledTask:
        return ScheduledTask(
            id=task_id,
            func=func,
            kwargs=kwargs,
            schedule=schedule,
        )
