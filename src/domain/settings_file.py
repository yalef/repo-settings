import dataclasses

from .schedule import Schedule


@dataclasses.dataclass
class Label:
    name: str
    description: str
    color: str

    def __eq__(self, o):
        if o.name == self.name:
            return True
        return False


@dataclasses.dataclass
class RepositorySection:
    description: str


@dataclasses.dataclass
class Settings:
    repository: RepositorySection
    labels: list[Label]
    schedule: Schedule
