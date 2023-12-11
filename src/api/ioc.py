import src.domain
import src.adapters
import src.application
import contextlib


class IoC:
    def __init__(self, settings):
        self._settings = settings

    @contextlib.contextmanager
    def init_repo_client(self, name: str, owner: str, installation_id: int):
        yield src.adapters.GithubRepositoryGateway(
            installation_id=installation_id,
            app_id=self._settings.app_id,
            app_private_key=self._settings.app_private_key,
            repository_name=name,
            owner_name=owner,
        )

    @contextlib.contextmanager
    def handle_push_payload(
        self,
        gateway: src.adapters.GithubRepositoryGateway,
    ):
        yield src.application.PushHandler(
            git_gateway=gateway,
            label_service=src.domain.LabelService(),
        )
