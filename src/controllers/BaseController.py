from ..helpers.config import load_settings, Settings

class BaseController:
    def __init__(self, settings: Settings = None):
        self.settings = settings or load_settings() 
        
    def get_app_info(self) -> dict:
        return {
            "app_name": self.settings.APP_NAME,
            "app_version": self.settings.APP_VERSION
        }