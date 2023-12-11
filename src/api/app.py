import fastapi
import src.settings
from . import router
from . import ioc


def singleton(value):
    def factory():
        return value
    return factory


settings = src.settings.Settings()
container = ioc.IoC(settings=settings)
app = fastapi.FastAPI()
app.dependency_overrides.update({
    ioc.IoC: singleton(container),
})
app.include_router(router.router, prefix="")
