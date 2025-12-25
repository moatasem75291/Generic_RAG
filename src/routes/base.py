from fastapi import FastAPI, APIRouter, Depends
import logging
from ..helpers.config import load_settings, Settings

router = APIRouter(
    prefix="/api/v1",
    tags=["Base"],
)

logger = logging.getLogger(__name__)

@router.get("/")
async def read_root(settings: Settings = Depends(load_settings)):
    title = settings.APP_NAME
    version = settings.APP_VERSION
    text = f"Welcome to the {title} application! Version: {version}"
    logger.info(text)
    return {
        "message": text,
        "app Name": title,
        "version": version
    }