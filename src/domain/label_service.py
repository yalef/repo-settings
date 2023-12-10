from . import settings_file


class LabelService:
    def create_label(
        self,
        name: str,
        description: str,
        color: str,
    ) -> settings_file.Label:
        return settings_file.Label(
            id=None,
            name=name,
            description=description,
            color=color,
        )

    def find_labels_for_delete(
        self,
        settings_labels: list[settings_file.Label],
        existing_labels: list[settings_file.Label],
    ):
        delete_labels = []
        for existing_label in existing_labels:
            if existing_label not in settings_labels:
                delete_labels.append(existing_label)

        return delete_labels
