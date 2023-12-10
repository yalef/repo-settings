import github


class GithhubInstallationGateway:
    def __init__(
        self,
        app_id: int,
        app_private_key: str,
        installation_id: int,
    ):
        self._app_auth = github.Auth.AppAuth(
            app_id=app_id,
            private_key=app_private_key,
        )
        self._installation_auth = self._app_auth.get_installation_auth(
            installation_id=installation_id,
        )
        self._client = github.Github(auth=self._installation_auth)
