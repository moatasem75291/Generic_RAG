from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import logging
import os
import dotenv
from fastapi.middleware.cors import CORSMiddleware
from .routes.base import router as base_router
from .routes.data import router as data_router


dotenv.load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
title = os.getenv("APP_NAME", "My FastAPI Application")
version = os.getenv("APP_VERSION", "1.0.0")

app = FastAPI(
    title=title,
    version=version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base_router)
app.include_router(data_router)