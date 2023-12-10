import typing


class RepositoryWriter(typing.Protocol):
    def update_description(
        self,
        description: str,
    ):
        pass
