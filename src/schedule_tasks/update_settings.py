import src.application
import src.adapters
import src.domain
import src.settings


def update_settings(owner: str, repo: str):
    settings = src.settings.Settings()
    git_gateway = src.adapters.GithubRepositoryGateway(
        app_id=settings.app_id,
        app_private_key=settings.app_private_key,
        repository_name=repo,
        owner_name=owner,
        schedule_service=src.domain.ScheduleService(),
    )
    updater = src.application.settings_update.SettingsUpdate(
        git_gateway,
        src.domain.LabelService(),
    )
    updater()
