import enum
import collections.abc
import pydantic

from .base import Repository, Installation


class Sender(pydantic.BaseModel):
    id: int
    login: str


class InstallationActions(enum.StrEnum):
    created = "added"
    removed = "removed"


class RepositorySelection(enum.StrEnum):
    all = "all"
    selected = "selected"


class InstallationWebhook(pydantic.BaseModel):
    """Webhook for installation event."""

    action: InstallationActions
    installation: Installation
    repositories_added: collections.abc.Iterable[Repository]
    repositories_removed: collections.abc.Iterable[Repository]
    repository_selection: RepositorySelection
    sender: Sender
