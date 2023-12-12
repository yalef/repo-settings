import dataclasses


@dataclasses.dataclass
class Schedule:
    minute: str
    hour: str
    month_day: str
    week_day: str
    month: str
