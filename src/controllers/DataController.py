from ..controllers.BaseController import BaseController
from fastapi import UploadFile

class DataController(BaseController):
    def __init__(self, settings=None):
        super().__init__(settings)


    def validate_uploaded_file(self, file: UploadFile) -> bool:
        allowed_extensions = self.settings.FILE_ALLOWED_EXTENSIONS
        max_size_mb = self.settings.MAX_FILE_SIZE_MB
        
        if file.content_type not in allowed_extensions:
            return False
        
        file_size_mb = len(file.file.read()) / (1024 * 1024)
        file.file.seek(0)  # Reset file pointer after reading
        
        if file_size_mb > max_size_mb:
            return False
        
        return True