from . import protocols


class TaskGateway(
    protocols.TaskDeleter,
    protocols.TaskWriter,
    protocols.TaskReader,
):
    pass


class TaskDelete:
    def __init__(
        self,
        task_gateway: TaskGateway,
    ):
        self._task_gateway = task_gateway

    def __call__(self, repository: protocols.RepositoryPayload):
        self._task_gateway.delete_task(repository.full_name)
