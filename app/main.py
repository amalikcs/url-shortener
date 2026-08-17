from fastapi import FastAPI

from app.core.config import settings

from app.api.routes.url import router

app = FastAPI(title=settings.app_name)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": settings.app_name
    }