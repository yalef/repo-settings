import typing
import pydantic


class Repository(pydantic.BaseModel):
    name: str
    full_name: str
    id: int
    node_id: str
    private: bool


class Installation(pydantic.BaseModel):
    id: int


class User(pydantic.BaseModel):
    email: pydantic.EmailStr | None
    name: str


class Commit(pydantic.BaseModel):
    added: list[str] | None
    modified: list[str] | None
    removed: list[str] | None
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
    commits: list[Commit]
    head_commit: Commit | None
    compare: pydantic.AnyHttpUrl
    created: bool
    deleted: bool
    forced: bool
    ref: str
    repository: Repository
    installation: Installation


class InstallationWebhook(pydantic.BaseModel):
    action: typing.Literal["added"] | typing.Literal["removed"]
    installation: Installation
    repositories_added: list[Repository]
    repositories_removed: list[Repository]
