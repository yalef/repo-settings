import contextlib

import src.adapters
import src.application
import src.domain


class IoC:
    def __init__(self, settings, scheduler):
        self._settings = settings
        self._task_gateway = src.adapters.APSchedulerGateway(scheduler)

    @contextlib.contextmanager
    def init_repo_client(self, name: str, owner: str, installation_id: int):
        yield src.adapters.GithubRepositoryGateway(
            installation_id=installation_id,
            app_id=self._settings.app_id,
            app_private_key=self._settings.app_private_key,
            repository_name=name,
            owner_name=owner,
            schedule_service=src.domain.ScheduleService(),
        )

    @contextlib.contextmanager
    def handle_push_payload(
        self,
        gateway: src.adapters.GithubRepositoryGateway,
    ):
        yield src.application.PushHandler(
            git_gateway=gateway,
            task_gateway=self._task_gateway,
            label_service=src.domain.LabelService(),
            task_service=src.domain.ScheduledTaskService(),
        )
