from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_EXTENSIONS: list[str]
    MAX_FILE_SIZE_MB: int

    class Config:
        env_file = "src/.env"
        env_file_encoding = "utf-8"
        model_config = SettingsConfigDict(arbitrary_types_allowed=True)
        
        
def load_settings() -> Settings:
    return Settings()