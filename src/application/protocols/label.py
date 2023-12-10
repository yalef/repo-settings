import src.domain
import typing


class LabelWriter(typing.Protocol):
    def get_labels(self) -> list[src.domain.Label]:
        ...

    def save_label(self, label: src.domain.Label):
        ...

    def delete_label(self, label_name: str):
        ...
