import fastapi
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import src.settings
from src.api import ioc, router


def singleton(value):
    def factory():
        return value

    return factory


settings = src.settings.Settings()
scheduler = AsyncIOScheduler()
scheduler.start()
container = ioc.IoC(settings=settings, scheduler=scheduler)
app = fastapi.FastAPI()
app.dependency_overrides.update(
    {
        ioc.IoC: singleton(container),
    }
)
app.include_router(router.router, prefix="")
