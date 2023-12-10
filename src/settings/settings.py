import pydantic_settings
import pydantic


class Settings(pydantic_settings.BaseSettings):
    app_id: int
    app_private_key: str
    webhook_url: pydantic.AnyHttpUrl

    model_config = pydantic_settings.SettingsConfigDict(env_file=".env")