from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/")
def home():
    return {
        "message": settings.app_name
    }