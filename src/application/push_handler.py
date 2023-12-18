from . import protocols
from .payload_validate import PushPayloadValidator
from .settings_update import SettingsUpdate
from .task_create import TaskCreate


class PushHandler:
    def __init__(
        self,
        validator: PushPayloadValidator,
        updater: SettingsUpdate,
        task_creator: TaskCreate,
    ):
        self._validator = validator
        self._updater = updater
        self._task_creator = task_creator

    def __call__(
        self,
        payload: protocols.PushPayload,
    ):
        if not self._validator(payload):
            return
        schedule = self._updater().schedule
        owner, repo = payload.repository.full_name.split("/")
        self._task_creator(
            schedule,
            task_id=payload.repository.full_name,
            owner=owner,
            repo=repo,
        )
