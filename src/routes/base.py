from fastapi import FastAPI, APIRouter
import dotenv
import logging
import os

router = APIRouter(
    prefix="/api/v1",
    tags=["Base"],
)


dotenv.load_dotenv()

title = os.getenv("APP_NAME", "My FastAPI Application")
version = os.getenv("APP_VERSION", "1.0.0")

logger = logging.getLogger(__name__)

@router.get("/")
async def read_root():
    text = f"Welcome to the {title} application! Version: {version}"
    logger.info(text)
    return {
        "message": text,
        "app Name": title,
        "version": version
    }