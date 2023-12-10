import fastapi
from . import router


app = fastapi.FastAPI()
app.include_router(router.router, prefix="")
