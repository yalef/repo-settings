import src.domain
from . import protocols


class PushGitGateway(
    protocols.SettingsFileReader,
    protocols.RepositoryWriter,
    protocols.LabelWriter,
):
    pass


class PushHandler:
    def __init__(
        self,
        git_gateway: PushGitGateway,
        label_service: src.domain.LabelService,
    ):
        self._git_gateway = git_gateway
        self._label_serivce = label_service

    def _check_settings_changed(
        self,
        commits: list[protocols.CommitPayload],
        ref: str,
    ):
        if (
            any(
                filter(
                    lambda commit: (
                        ".github/settings.yml" in commit.added + commit.modified
                    ),
                    commits,
                ),
            )
            and ref.split("/")[-1] == "main"
        ):
            return True
        return False

    def __call__(self, payload: protocols.PushPayload):
        # check if settings added/changed in main branch
        if not self._check_settings_changed(
            payload.commits,
            payload.ref,
        ):
            return
        # load settings
        new_settings = self._git_gateway.load_settings(
            file_path=".github/settings.yml",
        )
        # update description according loaded settings
        self._git_gateway.update_description(
            new_settings.repository.description,
        )
        # get deleted labels from label service
        labels_to_delete = self._label_serivce.find_labels_for_delete(
            settings_labels=new_settings.labels,
            existing_labels=self._git_gateway.get_labels(),
        )
        # delete labels
        for label in labels_to_delete:
            self._git_gateway.delete_label(
                label_name=label.name,
            )
        # update/create rest of the labels
        for label in new_settings.labels:
            self._git_gateway.save_label(
                label=label,
            )
