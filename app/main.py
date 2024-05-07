from fastapi import FastAPI

from .admin import admin

app = FastAPI()


@app.get("/", include_in_schema=False)
def app_status() -> dict[str, str]:
    return dict(status="up")


admin.mount_to(app)
