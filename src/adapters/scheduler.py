from apscheduler.schedulers.asyncio import AsyncIOScheduler
import src.application.protocols
import src.domain


class APSchedulerGateway(
    src.application.protocols.TaskWriter,
    src.application.protocols.TaskDeleter,
    src.application.protocols.TaskReader,
):
    def __init__(self, scheduler: AsyncIOScheduler):
        self._scheduler = scheduler

    def get_tasks(self) -> list[src.domain.ScheduledTask]:
        tasks = self._scheduler.get_jobs()
        return [
            src.domain.ScheduledTask(
                task.id,
                task.func,
                task.kwargs,
                src.domain.Schedule(
                    task.trigger.minute,
                    task.trigger.hour,
                    task.trigger.day,
                    task.trigger.day_of_week,
                    task.trigger.month,
                ),
            )
            for task in tasks
        ]

    def get_task(self, task_id: str) -> src.domain.ScheduledTask:
        task = self._scheduler.get_job(task_id)
        if task is None:
            return None
        return src.domain.ScheduledTask(
            id=task.id,
            func=task.func,
            kwargs=task.kwargs,
            schedule=src.domain.Schedule(
                task.trigger.minute,
                task.trigger.hour,
                task.trigger.day,
                task.trigger.day_of_week,
                task.trigger.month,
            ),
        )

    def save_task(self, task: src.domain.ScheduledTask):
        existing_task = self.get_task(task.id)
        if existing_task is None:
            self._scheduler.add_job(
                task.func,
                kwargs=task.kwargs,
                id=task.id,
                trigger="cron",
                minute=task.schedule.minute,
                hour=task.schedule.hour,
                day_of_week=task.schedule.week_day,
                day=task.schedule.month_day,
                month=task.schedule.month,
            )
        else:
            self._scheduler.modify_job(
                job_id=existing_task.id,
                func=task.func,
                kwargs=task.kwargs,
                id=task.id,
                trigger="cron",
                minute=task.schedule.minute,
                hour=task.schedule.hour,
                day_of_week=task.schedule.week_day,
                day=task.schedule.month_day,
                month=task.schedule.month,
            )

    def delete_task(self, task_id: str):
        self._scheduler.remove_job(task_id)
