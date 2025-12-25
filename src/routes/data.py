from fastapi import FastAPI, APIRouter, Depends, UploadFile
import logging
from ..helpers.config import load_settings, Settings
from ..controllers.DataController import DataController

router = APIRouter(
    prefix="/api/v1/data",
    tags=["app_v1", "data"],
)

logger = logging.getLogger(__name__)

@router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    settings: Settings = Depends(load_settings)
):
    logger.info(f"Uploading data for project ID: {project_id}")
    # Here you would add the logic to handle the uploaded file
    
    is_valid = DataController(settings).validate_uploaded_file(file)
    
    return {
        "project_id": project_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "is_valid": is_valid
    }