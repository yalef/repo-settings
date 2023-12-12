import src.domain
import typing


class TaskWriter(typing.Protocol):
    def save_task(
        self,
        task: src.domain.ScheduledTask,
    ):
        ...


class TaskReader(typing.Protocol):
    def get_tasks(self):
        ...

    def get_task(self, task_id: str):
        ...


class TaskDeleter(typing.Protocol):
    def delete_task(self, task_id: str):
        ...
