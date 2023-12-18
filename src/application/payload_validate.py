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
