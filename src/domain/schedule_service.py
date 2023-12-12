from .schedule import Schedule


class ScheduleService:
    def create_schedule(self, schedule_str: str) -> Schedule:
        ticks = schedule_str.split(" ")
        if len(ticks) > 5:
            ticks = ticks[:5]
        return Schedule(*ticks)
