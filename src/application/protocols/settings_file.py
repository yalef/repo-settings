import typing
import src.domain
from . import payload


class SettingsFileReader(typing.Protocol):
    def load_settings(
        self,
        file_path: payload.PushPayload,
    ) -> src.domain.Settings:
        pass
