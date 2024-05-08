from fastapi import FastAPI

from .admin import admin
from .spa.routers import services_router

app = FastAPI()
app.include_router(services_router)


@app.get("/", include_in_schema=False)
def app_status() -> dict[str, str]:
    return dict(status="up")


admin.mount_to(app)
