import contextlib

import rq
import rq_scheduler
import redis

import src.adapters
import src.application
import src.domain
import src.schedule_tasks


class IoC:
    def __init__(self, app_id: int, app_private_key: str):
        self._app_id = app_id
        self._app_private_key = app_private_key

    @contextlib.contextmanager
    def init_repo_client(self, name: str, owner: str, installation_id: int):
        yield src.adapters.GithubRepositoryGateway(
            app_id=self._app_id,
            app_private_key=self._app_private_key,
            repository_name=name,
            owner_name=owner,
            schedule_service=src.domain.ScheduleService(),
        )

    @contextlib.contextmanager
    def init_redis_connection(self):
        connection = redis.Redis()
        yield connection
        connection.close()

    @contextlib.contextmanager
    def init_redis_queue(
        self,
        connection: redis.Redis,
        queue_name: str = "settings_update",
    ):
        queue = rq.Queue(name=queue_name, connection=connection)
        yield queue

    @contextlib.contextmanager
    def init_redis_scheduler(
        self,
        connection: redis.Redis,
        queue: rq.Queue,
    ):
        scheduler = rq_scheduler.Scheduler(queue=queue, connection=connection)
        yield scheduler

    @contextlib.contextmanager
    def handle_push_payload(
        self,
        gateway: src.adapters.GithubRepositoryGateway,
        scheduler: rq_scheduler.Scheduler,
        queue: rq.Queue,
    ):
        task_gateway = src.adapters.RQSchedulerGateway(
            queue=queue,
            scheduler=scheduler,
            schedule_service=src.domain.ScheduleService(),
        )
        validator = src.application.PushPayloadValidator()
        settings_updater = src.application.SettingsUpdate(
            git_gateway=gateway,
            label_service=src.domain.LabelService(),
        )
        task_creator = src.application.TaskCreate(
            task_gateway=task_gateway,
            task_service=src.domain.ScheduledTaskService(),
            task=src.schedule_tasks.update_settings,
        )
        yield src.application.PushHandler(
            validator=validator,
            updater=settings_updater,
            task_creator=task_creator,
        )

    @contextlib.contextmanager
    def handle_installation_payload(
        self,
        scheduler: rq_scheduler.Scheduler,
        queue: rq.Queue,
    ):
        task_gateway = src.adapters.RQSchedulerGateway(
            queue=queue,
            scheduler=scheduler,
            schedule_service=src.domain.ScheduleService(),
        )
        validator = src.application.InstallationPayloadValidator()
        deleter = src.application.TaskDelete(
            task_gateway=task_gateway,
        )
        yield src.application.InstallationHandler(
            validator=validator,
            task_deleter=deleter,
        )
