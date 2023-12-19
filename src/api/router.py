import enum
import logging
import typing

import fastapi

from . import ioc, schema

router = fastapi.APIRouter()
logging.basicConfig(level=logging.DEBUG)


class EventTypes(enum.StrEnum):
    push = "push"
    installation = "installation_repositories"


@router.post("/")
def handle_webhook(
    webhook: schema.PushWebhook | schema.InstallationWebhook,
    x_github_event: typing.Annotated[EventTypes, fastapi.Header()],
    container: typing.Annotated[ioc.IoC, fastapi.Depends()],
) -> typing.Literal["OK"]:
    logging.info(f"HANDLED {x_github_event}")
    match x_github_event:
        case EventTypes.push:
            owner, repo_name = webhook.repository.full_name.split("/")
            with container.init_repo_client(
                repo_name,
                owner,
                webhook.installation.id,
            ) as repo_gateway:
                with container.init_redis_connection() as connection:
                    with container.init_redis_queue(connection) as queue:
                        with container.init_redis_scheduler(
                            queue=queue,
                            connection=connection,
                        ) as scheduler:
                            with container.handle_push_payload(
                                gateway=repo_gateway,
                                scheduler=scheduler,
                                queue=queue,
                            ) as push_handler:
                                push_handler(webhook)
        case EventTypes.installation:
            logging.info(f"HANDLED {x_github_event}")
            with container.init_redis_connection() as connection:
                with container.init_redis_queue(connection) as queue:
                    with container.init_redis_scheduler(
                        queue=queue,
                        connection=connection,
                    ) as scheduler:
                        with container.handle_installation_payload(
                            scheduler=scheduler,
                            queue=queue,
                        ) as installation_handler:
                            installation_handler(webhook)
    return "OK"
