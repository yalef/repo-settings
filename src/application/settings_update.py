import src.domain

from . import protocols


class PushGitGateway(
    protocols.SettingsFileReader,
    protocols.RepositoryWriter,
    protocols.LabelWriter,
):
    pass


class SettingsUpdate:
    def __init__(
        self,
        git_gateway: PushGitGateway,
        label_service: src.domain.LabelService,
    ):
        self._git_gateway = git_gateway
        self._label_serivce = label_service

    def __call__(self):
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
        return new_settings
