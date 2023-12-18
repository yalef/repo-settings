import fastapi

import src.settings
from src.api import ioc, router


def singleton(value):
    def factory():
        return value

    return factory


settings = src.settings.Settings()
container = ioc.IoC(
    app_id=settings.app_id,
    app_private_key=settings.app_private_key,
)
app = fastapi.FastAPI()
app.dependency_overrides.update(
    {
        ioc.IoC: singleton(container),
    }
)
app.include_router(router.router, prefix="")
