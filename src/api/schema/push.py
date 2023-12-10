import pydantic
import collections.abc
from .base import Repository, Installation


class User(pydantic.BaseModel):
    email: pydantic.EmailStr | None
    name: str


class Commit(pydantic.BaseModel):
    added: collections.abc.Sequence[str] | None
    modified: collections.abc.Sequence[str] | None
    removed: collections.abc.Sequence[str] | None
    author: User
    committer: User
    distinct: bool
    id: str
    message: str
    timestamp: str
    tree_id: str
    url: pydantic.AnyHttpUrl


class PushWebhook(pydantic.BaseModel):
    """Webhook for push event."""

    after: str
    before: str
    base_ref: str | None
    commits: collections.abc.Iterable[Commit]
    head_commit: Commit | None
    compare: pydantic.AnyHttpUrl
    created: bool
    deleted: bool
    forced: bool
    ref: str
    repository: Repository
    installation: Installation
