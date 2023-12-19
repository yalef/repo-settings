import typing


class RepositoryPayload(typing.Protocol):
    id: int
    full_name: str


class CommitPayload(typing.Protocol):
    added: list[str] | None
    modified: list[str] | None
    removed: list[str] | None


class PushPayload(typing.Protocol):
    ref: str
    commits: list[CommitPayload]
    repository: RepositoryPayload


class InstallationPayload(typing.Protocol):
    action: str
    repositories_added: list[RepositoryPayload]
    repositories_removed: list[RepositoryPayload]
