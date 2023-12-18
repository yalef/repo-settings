import typing
import src.domain

from . import protocols


class TaskGateway(
    protocols.TaskDeleter,
    protocols.TaskWriter,
    protocols.TaskReader,
):
    pass


class TaskCreate:
    def __init__(
        self,
        task_gateway: TaskGateway,
        task_service: src.domain.ScheduledTaskService,
        task: typing.Callable,
    ):
        self._task_gateway = task_gateway
        self._task_service = task_service
        self._task = task

    def __call__(
        self,
        schedule: src.domain.Schedule,
        task_id: str,
        **task_kwargs,
    ):
        new_task = self._task_service.create_task(
            task_id=task_id,
            func=self._task,
            kwargs=task_kwargs,
            schedule=schedule,
        )
        self._task_gateway.save_task(
            new_task,
        )
