import yaml
import github
import src.domain
import src.application.protocols as application_protocols
from . import github_session_provider


class GithubRepositoryGateway(
    github_session_provider.GithhubInstallationGateway,
    application_protocols.LabelWriter,
    application_protocols.RepositoryWriter,
    application_protocols.SettingsFileReader,
):
    def __init__(
        self,
        repository_name: str,
        owner_name: str,
        schedule_service: src.domain.ScheduleService,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._repo = self._client.get_repo(f"{owner_name}/{repository_name}")
        self._schedule_service = schedule_service

    def get_labels(self) -> list[src.domain.Label]:
        return [
            src.domain.Label(
                name=label.name,
                description=label.description,
                color=label.color,
            )
            for label in self._repo.get_labels()
        ]

    def save_label(
        self,
        label: src.domain.Label,
    ):
        try:
            existing_label = self._repo.get_label(label.name)
            existing_label.edit(
                name=label.name,
                color=label.color,
                description=label.description,
            )
        except github.GithubException:
            self._repo.create_label(
                name=label.name,
                color=label.color,
                description=label.description,
            )

    def delete_label(
        self,
        label_name: str,
    ):
        self._repo.get_label(label_name).delete()

    def update_description(
        self,
        description: str,
    ):
        self._repo.edit(
            description=description,
        )

    def load_settings(
        self,
        file_path: str,
        branch: str = "main",
    ) -> src.domain.Settings:
        settings_dict = yaml.safe_load(
            self._repo.get_contents(
                path=file_path,
                ref=branch,
            ).decoded_content.decode(),
        )
        return src.domain.Settings(
            repository=src.domain.RepositorySection(
                description=settings_dict["repository"]["description"],
            ),
            labels=[
                src.domain.Label(
                    name=label["name"],
                    description=label["description"],
                    color=label["color"],
                )
                for label in settings_dict["labels"]
            ],
            schedule=self._schedule_service.create_schedule(
                settings_dict["schedule"],
            ),
        )
