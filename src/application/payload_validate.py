from . import protocols


class PushPayloadValidator:
    def __call__(self, payload: protocols.PushPayload):
        if (
            any(
                filter(
                    lambda commit: (
                        ".github/settings.yml"
                        in commit.added + commit.modified
                    ),
                    payload.commits,
                ),
            )
            and payload.ref.split("/")[-1] == "main"
        ):
            return True
        return False


class InstallationPayloadValidator:
    def __call__(self, payload: protocols.InstallationPayload):
        if (
            payload.action != "removed"
            or len(payload.repositories_removed) == 0
        ):
            return False
        return True
