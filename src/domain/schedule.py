import dataclasses


@dataclasses.dataclass
class Schedule:
    minute: str
    hour: str
    month_day: str
    week_day: str
    month: str

    @property
    def cron_string(self) -> str:
        return (
            f"{self.minute} {self.hour} {self.month_day} "
            f"{self.month} {self.week_day}"
        )
