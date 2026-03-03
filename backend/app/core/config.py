from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "AI Posture Analysis Service"
    VERSION: str = "1.0.0"

    ALLOWED_ORIGINS: List[str] = ["*"]

    MIN_VIDEO_DURATION: int = 10
    MAX_VIDEO_DURATION: int = 15

    SUPPORTED_FORMATS: List[str] = ["mp4", "mov", "avi"]

    STORAGE_ROOT: str = "storage"
    TEMP_FOLDER: str = "storage/temp"
    IMAGE_FOLDER: str = "storage/images"
    REPORT_FOLDER: str = "storage/reports"
    ANALYSIS_FOLDER: str = "storage/analysis"
    VIDEO_FOLDER: str = "storage/videos"

    FRAME_SAMPLING_RATE: int = 5

    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


settings = Settings()