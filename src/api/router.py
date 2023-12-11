from . import schema
from . import ioc
import typing
import enum
import fastapi

import logging


router = fastapi.APIRouter()
logging.basicConfig(level=logging.DEBUG)


class EventTypes(enum.StrEnum):
    push = "push"


@router.post("/")
def handle_webhook(
    webhook: schema.PushWebhook,
    x_github_event: typing.Annotated[EventTypes, fastapi.Header()],
    container: typing.Annotated[ioc.IoC, fastapi.Depends()]
) -> typing.Literal["OK"]:
    logging.info(f"HANDLED {x_github_event}")
    owner, repo_name = webhook.repository.full_name.split("/")
    with container.init_repo_client(
        repo_name,
        owner,
        webhook.installation.id,
    ) as repo_gateway:
        with container.handle_push_payload(repo_gateway) as push_handler:
            push_handler(webhook)
    return "OK"
