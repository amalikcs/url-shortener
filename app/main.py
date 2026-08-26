from fastapi import FastAPI
import logging

from app.core.config import settings
from app.api.routes.url import router
from app.core import logger

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

app.include_router(router)

@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {
        "message": settings.app_name
    }