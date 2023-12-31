import rq
import rq_scheduler

import src.application.protocols
import src.domain


class RQSchedulerGateway(
    src.application.protocols.TaskWriter,
    src.application.protocols.TaskDeleter,
    src.application.protocols.TaskReader,
):
    def __init__(
        self,
        scheduler: rq_scheduler.Scheduler,
        queue: rq.Queue,
        schedule_service: src.domain.ScheduleService,
    ):
        self._scheduler = scheduler
        self._queue = queue
        self._schedule_service = schedule_service

    def _parse_redis_task(self, task: rq.job.Job) -> src.domain.ScheduledTask:
        schedule = self._schedule_service.create_schedule(
            task.meta["cron_string"],
        )
        return src.domain.ScheduledTask(
            id=task.id,
            func=task.func,
            kwargs=task.kwargs,
            schedule=schedule,
        )

    def get_tasks(self) -> list[src.domain.ScheduledTask]:
        _tasks = self._scheduler.get_jobs()
        return [self._parse_redis_task(task) for task in _tasks]

    def get_tasks_by_id(self, task_id: str) -> list[src.domain.ScheduledTask]:
        tasks = self.get_tasks()
        result = []
        for task in tasks:
            if task.id == task_id:
                result.append(task)
        return result

    def save_task(self, task: src.domain.ScheduledTask):
        existing_tasks = self.get_tasks_by_id(task.id)
        for task in existing_tasks:
            self.delete_task(task.id)

        self._scheduler.cron(
            id=task.id,
            cron_string=task.schedule.cron_string,
            func=task.func,
            kwargs=task.kwargs,
        )

    def delete_task(self, task_id: str):
        jobs = self._scheduler.get_jobs()
        for job in jobs:
            if job.id == task_id:
                self._scheduler.cancel(job)
