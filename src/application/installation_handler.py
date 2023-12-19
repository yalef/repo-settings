from .task_delete import TaskDelete
from .payload_validate import InstallationPayloadValidator
from . import protocols


class InstallationHandler:
    def __init__(
        self,
        validator: InstallationPayloadValidator,
        task_deleter: TaskDelete,
    ):
        self._validator = validator
        self._deleter = task_deleter

    def __call__(self, payload: protocols.InstallationPayload):
        if not self._validator(payload):
            return
        for repo in payload.repositories_removed:
            self._deleter(repo)
