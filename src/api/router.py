from . import schema
import src.settings
import src.application
import src.adapters
import src.domain
import typing
import enum
import fastapi

import logging


router = fastapi.APIRouter()
logging.basicConfig(level=logging.DEBUG)


class EventTypes(enum.StrEnum):
    push = "push"
    installation_repositories = "installation_repositories"


@router.post("/")
def handle_webhook(
    webhook: schema.PushWebhook | schema.InstallationWebhook,
    x_github_event: typing.Annotated[EventTypes, fastapi.Header()],
):
    settings = src.settings.Settings()
    logging.info(f"HANDLED {x_github_event}")
    match x_github_event:
        case EventTypes.push:
            logging.info(f"MATCHED {x_github_event}")
            owner, repo_name = webhook.repository.full_name.split("/")
            push_gateway = src.adapters.GithubRepositoryGateway(
                repository_name=repo_name,
                owner_name=owner,
                app_id=settings.app_id,
                app_private_key=settings.app_private_key,
                installation_id=webhook.installation.id,
            )
            interactor = src.application.PushHandler(
                git_gateway=push_gateway,
                payload=webhook,
                label_service=src.domain.LabelService(),
            )
            interactor()
        # case EventTypes.installation_repositories:
        #     installation_gateway = src.adapters.GithubInstallationGateway(
        #         app_id=settings.app_id,
        #         app_private_key=settings.app_private_key,
        #         installation_id=webhook.installation.id,
        #     )
        #     interactor = src.application.InstallationHandler(
        #         settings=settings,
        #         git_gateway=installation_gateway,
        #         payload=webhook,
        #         webhook_service=src.domain.WebhookService(),
        #     )
        #     interactor()
        case _:
            pass
    return "OK"
